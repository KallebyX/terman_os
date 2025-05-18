from flask import render_template
from flask_login import login_required
from app.decorators import admin_required
from app.models.pedido import Pedido
from app.routes.admin import admin_bp

@admin_bp.route("/pedidos")
@login_required
@admin_required
def listar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.data_criacao.desc()).all()
    return render_template("admin/pedidos/listar.html", pedidos=pedidos)

@admin_bp.route("/pedidos/<int:id>")
@login_required
@admin_required
def visualizar_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    return render_template("admin/pedidos/visualizar.html", pedido=pedido)