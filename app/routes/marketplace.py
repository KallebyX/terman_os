from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from flask_login import login_required, current_user
from app.models.produto import Produto
from app.models.pedido import Pedido, ItemPedido
from app import db

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/')
def loja():
    produtos = Produto.query.all()
    return render_template('loja.html', produtos=produtos)

@marketplace_bp.route('/produto/<int:produto_id>')
def produto_detalhado(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('produto.html', produto=produto)

@marketplace_bp.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', {})
    itens = []
    total = 0
    for pid, item in carrinho.items():
        produto = Produto.query.get(int(pid))
        subtotal = produto.preco * item['quantidade']
        total += subtotal
        itens.append({
            'produto': produto,
            'quantidade': item['quantidade'],
            'subtotal': subtotal,
            'produto_id': produto.id
        })
    return render_template('carrinho.html', itens=itens, total=total)

@marketplace_bp.route('/adicionar_carrinho/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    quantidade = int(request.form.get('quantidade', 1))
    carrinho = session.get('carrinho', {})
    if str(produto_id) in carrinho:
        carrinho[str(produto_id)]['quantidade'] += quantidade
    else:
        carrinho[str(produto_id)] = { 'quantidade': quantidade }
    session['carrinho'] = carrinho
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('marketplace.carrinho'))

@marketplace_bp.route('/remover_item_carrinho/<int:produto_id>', methods=['POST'])
def remover_item_carrinho(produto_id):
    carrinho = session.get('carrinho', {})
    carrinho.pop(str(produto_id), None)
    session['carrinho'] = carrinho
    flash('Item removido do carrinho.', 'info')
    return redirect(url_for('marketplace.carrinho'))

@marketplace_bp.route('/finalizar_pedido', methods=['POST'])
@login_required
def finalizar_pedido():
    carrinho = session.get('carrinho', {})
    if not carrinho:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('marketplace.loja'))

    pedido = Pedido(usuario_id=current_user.id)
    db.session.add(pedido)
    db.session.flush()

    for pid, item in carrinho.items():
        produto = Produto.query.get(int(pid))
        if produto.estoque < item['quantidade']:
            flash(f'Estoque insuficiente para o produto {produto.nome}.', 'danger')
            return redirect(url_for('marketplace.carrinho'))

        produto.estoque -= item['quantidade']

        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=item['quantidade'],
            preco_unitario=produto.preco
        )
        db.session.add(item_pedido)

    db.session.commit()
    session.pop('carrinho', None)
    flash('Pedido finalizado com sucesso!', 'success')
    return redirect(url_for('cliente.meus_pedidos'))