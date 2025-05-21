from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.models.user import User
from app import db
from . import auth_bp
from datetime import datetime
from urllib.parse import urlparse

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.ultimo_acesso = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                if user.tipo == 'admin':
                    next_page = url_for('admin.dashboard')
                elif user.tipo == 'cliente':
                    next_page = url_for('cliente.perfil')
                else:
                    next_page = url_for('pdv.dashboard')
            return redirect(next_page)
            
        flash('Email ou senha inválidos', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')) 