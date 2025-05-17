from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models.produto import Produto
from app import db
from app.decorators import admin_required
from app.models.categoria import Categoria
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

# Rota do dashboard admin
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/')
@login_required
@admin_required
def painel_admin():
    return render_template('index.html')

@admin_bp.route('/produtos')
@login_required
@admin_required
def listar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos/listar.html', produtos=produtos)

@admin_bp.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def criar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        estoque = int(request.form['estoque'])
        categoria_id = int(request.form['categoria_id'])
        imagem = request.files.get('imagem')

        imagem_filename = None
        if imagem and imagem.filename:
            imagem_filename = secure_filename(imagem.filename)
            caminho = os.path.join('app/static/produtos', imagem_filename)
            imagem.save(caminho)

        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            imagem_filename=imagem_filename,
            categoria_id=categoria_id
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('admin.listar_produtos'))

    categorias = Categoria.query.all()
    return render_template('produtos/novo.html', categorias=categorias)

@admin_bp.route('/produtos/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])
        produto.estoque = int(request.form['estoque'])
        produto.categoria_id = int(request.form['categoria_id'])
        imagem = request.files.get('imagem')

        if imagem and imagem.filename:
            imagem_filename = secure_filename(imagem.filename)
            caminho = os.path.join('app/static/produtos', imagem_filename)
            imagem.save(caminho)
            produto.imagem_filename = imagem_filename

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.listar_produtos'))

    categorias = Categoria.query.all()
    return render_template('produtos/editar.html', produto=produto, categorias=categorias)

@admin_bp.route('/produtos/excluir/<int:produto_id>', methods=['POST'])
@login_required
@admin_required
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'info')
    return redirect(url_for('admin.listar_produtos'))


# Rotas CRUD de categorias
@admin_bp.route('/categorias')
@login_required
@admin_required
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias/listar.html', categorias=categorias)

@admin_bp.route('/categorias/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        if Categoria.query.filter_by(nome=nome).first():
            flash('Categoria já existe.', 'warning')
        else:
            nova = Categoria(nome=nome)
            db.session.add(nova)
            db.session.commit()
            flash('Categoria criada com sucesso!', 'success')
            return redirect(url_for('admin.listar_categorias'))
    return render_template('categorias/novo.html')

@admin_bp.route('/categorias/editar/<int:categoria_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    if request.method == 'POST':
        categoria.nome = request.form['nome']
        db.session.commit()
        flash('Categoria atualizada!', 'success')
        return redirect(url_for('admin.listar_categorias'))
    return render_template('categorias/editar.html', categoria=categoria)

@admin_bp.route('/categorias/excluir/<int:categoria_id>', methods=['POST'])
@login_required
@admin_required
def excluir_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoria excluída!', 'info')
    return redirect(url_for('admin.listar_categorias')
)

from app.models.pedido import Pedido, ItemPedido

@admin_bp.route('/pedidos')
@login_required
@admin_required
def listar_pedidos_admin():
    pedidos = Pedido.query.order_by(Pedido.data_criacao.desc()).all()
    return render_template('pedidos/admin_listar.html', pedidos=pedidos)


# Visualizar pedido específico para admin
@admin_bp.route('/pedidos/<int:pedido_id>')
@login_required
@admin_required
def visualizar_pedido_admin(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('pedidos/visualizar_admin.html', pedido=pedido)