from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.cliente import Cliente
from app.models.produto import Produto
from app import db
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo != 'admin':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/clientes')
@login_required
def clientes():
    if current_user.tipo != 'admin':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
        
    clientes = Cliente.query.all()
    return render_template('admin/clientes.html', clientes=clientes)

@admin_bp.route('/produtos', methods=['GET', 'POST'])
@login_required
def produtos():
    if current_user.tipo != 'admin':
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        produto = Produto(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            preco=request.form['preco'],
            estoque=request.form['estoque']
        )
        
        try:
            db.session.add(produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
        except:
            db.session.rollback()
            flash('Erro ao cadastrar produto', 'error')
            
    produtos = Produto.query.all()
    return render_template('admin/produtos.html', produtos=produtos) 