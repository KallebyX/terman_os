from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.pedido import Pedido
from app.forms.editar_perfil_form import EditarPerfilForm
from app import db

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

@cliente_bp.route('/pedido/<int:pedido_id>')
@login_required
def visualizar_pedido(pedido_id):
    pedido = Pedido.query.filter_by(id=pedido_id, usuario_id=current_user.id).first_or_404()
    return render_template('pedidos/visualizar.html', pedido=pedido)

@cliente_bp.route('/perfil')
@login_required
def perfil():
    # Permitir acesso para todos os tipos de usuario autenticados
    return render_template('cliente/perfil.html', usuario=current_user)

@cliente_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    # Permitir acesso para todos os tipos de usuario autenticados

    form = EditarPerfilForm(obj=current_user)
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.email = form.email.data
        if form.senha.data:
            current_user.set_senha(form.senha.data)
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('cliente.perfil'))
    return render_template('cliente/editar_perfil.html', form=form)


# Rotas para rastreamento de pedido e exclusão de conta
import requests
from bs4 import BeautifulSoup

@cliente_bp.route('/pedido/<int:pedido_id>/rastrear')
@login_required
def rastrear_pedido(pedido_id):
    pedido = Pedido.query.filter_by(id=pedido_id, usuario_id=current_user.id).first_or_404()
    if not pedido.codigo_rastreio:
        flash("Este pedido ainda não possui código de rastreio.", "warning")
        return redirect(url_for('cliente.visualizar_pedido', pedido_id=pedido_id))

    url = f"https://www.linkcorreios.com.br/?id={pedido.codigo_rastreio}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    resultado = soup.find_all("ul", class_="linha_status")

    status = resultado[0].text.strip() if resultado else "Status não encontrado."
    return render_template('pedidos/rastrear.html', pedido=pedido, status=status)


@cliente_bp.route('/perfil/excluir', methods=['GET', 'POST'])
@login_required
def excluir_conta():
    # Apenas clientes podem excluir sua propria conta
    if current_user.tipo_usuario != 'cliente':
        flash("Administradores nao podem excluir sua conta por aqui.", "warning")
        return redirect(url_for('cliente.perfil'))

    if request.method == 'POST':
        pedidos = Pedido.query.filter_by(usuario_id=current_user.id).all()
        for p in pedidos:
            db.session.delete(p)
        db.session.delete(current_user)
        db.session.commit()
        flash("Conta excluída com sucesso.", "success")
        return redirect(url_for('auth.login'))

    return render_template('cliente/excluir_conta.html')