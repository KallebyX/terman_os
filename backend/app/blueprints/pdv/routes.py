from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from app.models.pedido import Pedido, ItemPedido
from app.models.produto import Produto
from app import db
from . import pdv_bp

@pdv_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo != 'funcionario':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
    return render_template('pdv/dashboard.html')

@pdv_bp.route('/venda', methods=['GET', 'POST'])
@login_required
def nova_venda():
    if current_user.tipo != 'funcionario':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        data = request.get_json()
        
        pedido = Pedido(
            cliente_id=data['cliente_id'],
            valor_total=data['valor_total']
        )
        
        try:
            db.session.add(pedido)
            
            for item in data['itens']:
                item_pedido = ItemPedido(
                    pedido=pedido,
                    produto_id=item['produto_id'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario']
                )
                db.session.add(item_pedido)
                
                # Atualizar estoque
                produto = Produto.query.get(item['produto_id'])
                produto.estoque -= item['quantidade']
                
            db.session.commit()
            return jsonify({'status': 'success', 'pedido_id': pedido.id})
        except:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': 'Erro ao processar venda'})
            
    produtos = Produto.query.filter_by(ativo=True).all()
    return render_template('pdv/venda.html', produtos=produtos) 