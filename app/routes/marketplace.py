from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from flask_login import login_required, current_user
from app.models.produto import Produto
from app.models.pedido import Pedido, ItemPedido
from app.models.categoria import Categoria
from app import db, cache
from app.utils import paginate_query
from sqlalchemy import or_

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/')
@cache.cached(timeout=300, query_string=True)
def loja():
    """Loja com busca, filtros e paginação"""
    # Parâmetros de busca e filtro
    search = request.args.get('q', '').strip()
    categoria_id = request.args.get('categoria', type=int)
    min_preco = request.args.get('min_preco', type=float)
    max_preco = request.args.get('max_preco', type=float)
    ordenar = request.args.get('ordenar', 'nome')  # nome, preco_asc, preco_desc, mais_vendidos
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # Query base - apenas produtos ativos
    query = Produto.query.filter_by(ativo=True)

    # Busca por nome ou descrição
    if search:
        query = query.filter(
            or_(
                Produto.nome.ilike(f'%{search}%'),
                Produto.descricao.ilike(f'%{search}%'),
                Produto.descricao_curta.ilike(f'%{search}%')
            )
        )

    # Filtro por categoria
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)

    # Filtro por preço
    if min_preco is not None:
        query = query.filter(Produto.preco >= min_preco)
    if max_preco is not None:
        query = query.filter(Produto.preco <= max_preco)

    # Ordenação
    if ordenar == 'preco_asc':
        query = query.order_by(Produto.preco.asc())
    elif ordenar == 'preco_desc':
        query = query.order_by(Produto.preco.desc())
    elif ordenar == 'mais_vendidos':
        query = query.order_by(Produto.vendas_total.desc())
    elif ordenar == 'mais_recentes':
        query = query.order_by(Produto.data_criacao.desc())
    else:  # nome
        query = query.order_by(Produto.nome.asc())

    # Paginação
    pagination = paginate_query(query, page, per_page)

    # Carregar categorias para filtro
    categorias = Categoria.query.all()

    # Log da busca
    if search:
        current_app.logger.info(f"Busca realizada: '{search}' - {pagination['total']} resultados")

    return render_template(
        'loja.html',
        produtos=pagination['items'],
        pagination=pagination,
        categorias=categorias,
        search=search,
        categoria_id=categoria_id,
        min_preco=min_preco,
        max_preco=max_preco,
        ordenar=ordenar
    )

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