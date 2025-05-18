from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
from app.forms.login_form import LoginForm
from app.forms.cadastro_form import CadastroForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            flash('Login realizado com sucesso!', 'success')
            if usuario.tipo_usuario == 'admin':
                return redirect(url_for('admin.listar_produtos'))
            elif usuario.tipo_usuario == 'cliente':
                return redirect(url_for('cliente.perfil'))
            else:
                logout_user()
                flash('Tipo de usuário inválido.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Este e-mail já está cadastrado.', 'warning')
        else:
            try:
                novo_usuario = User(
                    nome=form.nome.data,
                    email=form.email.data,
                    tipo_usuario='cliente'
                )
                novo_usuario.set_senha(form.senha.data)
                db.session.add(novo_usuario)
                db.session.commit()
                flash('Cadastro realizado com sucesso. Faça o login.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao cadastrar usuário: {e}")
                flash('Erro ao cadastrar. Tente novamente mais tarde.', 'danger')
    return render_template('cadastro.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/test-db')
def testar_conexao_banco():
    try:
        usuarios = User.query.limit(5).all()
        return jsonify({
            "status": "Conexão bem-sucedida!",
            "usuarios_encontrados": len(usuarios)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "Erro ao conectar",
            "erro": str(e)
        }), 500

@auth_bp.route('/force-create')
def force_create_tables():
    if not current_app.config.get('DEBUG', False):
        return "🔒 Rota indisponível em produção."
    try:
        db.create_all()
        return "✅ Tabelas criadas no PostgreSQL remoto com sucesso!"
    except Exception as e:
        return f"❌ Erro ao criar tabelas: {str(e)}"