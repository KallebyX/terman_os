from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.pedido import Pedido

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/')
@login_required
def painel_cliente():
    return render_template('painel_cliente.html', usuario=current_user)

@cliente_bp.route('/pedidos')
@login_required
def meus_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.data_criacao.desc()).all()
    return render_template('pedidos/cliente_listar.html', pedidos=pedidos)