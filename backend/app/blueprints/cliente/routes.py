from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app import db
from . import cliente_bp

@cliente_bp.route('/perfil')
@login_required
def perfil():
    if current_user.tipo != 'cliente':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
    return render_template('cliente/perfil.html')

@cliente_bp.route('/pedidos')
@login_required
def pedidos():
    if current_user.tipo != 'cliente':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
        
    pedidos = Pedido.query.filter_by(cliente_id=current_user.cliente_profile.id).all()
    return render_template('cliente/pedidos.html', pedidos=pedidos)

@cliente_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        user = User(
            email=request.form['email'],
            nome=request.form['nome'],
            tipo='cliente'
        )
        user.set_password(request.form['password'])
        
        cliente = Cliente(
            user=user,
            cpf=request.form['cpf'],
            telefone=request.form['telefone'],
            endereco=request.form['endereco'],
            cidade=request.form['cidade'],
            estado=request.form['estado'],
            cep=request.form['cep']
        )
        
        try:
            db.session.add(user)
            db.session.add(cliente)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))
        except:
            db.session.rollback()
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            
    return render_template('cliente/cadastro.html') 