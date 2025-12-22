from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db, limiter, mail
from app.forms.login_form import LoginForm
from app.forms.cadastro_form import CadastroForm
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


def get_serializer():
    """Retorna serializer para tokens de reset de senha"""
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def send_reset_email(user, token):
    """Envia email de recuperação de senha"""
    try:
        reset_url = url_for('auth.reset_senha', token=token, _external=True)
        msg = Message(
            subject='Recuperação de Senha - Mangueiras Terman',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email]
        )
        msg.html = f'''
        <h2>Recuperação de Senha</h2>
        <p>Olá {user.nome},</p>
        <p>Recebemos uma solicitação para redefinir sua senha.</p>
        <p>Clique no link abaixo para criar uma nova senha:</p>
        <p><a href="{reset_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Redefinir Senha</a></p>
        <p>Ou copie e cole este link no seu navegador:</p>
        <p>{reset_url}</p>
        <p><strong>Este link expira em 1 hora.</strong></p>
        <p>Se você não solicitou esta recuperação, ignore este email.</p>
        <hr>
        <p><small>Mangueiras Terman LTDA</small></p>
        '''
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Erro ao enviar email de reset: {e}")
        return False

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = User.query.filter_by(email=form.email.data).first()
        if usuario and usuario.verificar_senha(form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            if usuario.tipo_usuario == 'admin':
                return redirect(next_page) if next_page else redirect(url_for('admin.listar_produtos'))
            elif usuario.tipo_usuario == 'cliente':
                return redirect(next_page) if next_page else redirect(url_for('cliente.perfil'))
            else:
                logout_user()
                flash('Tipo de usuário inválido.', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
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
                current_app.logger.error(f"Erro ao cadastrar usuário: {e}")
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
    current_app.logger.info("🔍 Testando conexão com o banco de dados...")
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
    current_app.logger.info("⚙️ Forçando criação de tabelas no banco.")
    try:
        db.create_all()
        return "✅ Tabelas criadas no PostgreSQL remoto com sucesso!"
    except Exception as e:
        return f"❌ Erro ao criar tabelas: {str(e)}"


@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
@limiter.limit("3 per hour")
def esqueci_senha():
    """Página de solicitação de recuperação de senha"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email:
            flash('Por favor, informe seu email.', 'warning')
            return render_template('esqueci_senha.html')

        user = User.query.filter_by(email=email).first()

        # Sempre mostra a mesma mensagem (segurança)
        flash('Se o email estiver cadastrado, você receberá instruções para recuperar sua senha.', 'info')

        if user:
            # Gerar token
            s = get_serializer()
            token = s.dumps(user.email, salt='password-reset-salt')

            # Enviar email
            if send_reset_email(user, token):
                current_app.logger.info(f"Email de reset enviado para: {email}")
            else:
                current_app.logger.error(f"Falha ao enviar email de reset para: {email}")

        return redirect(url_for('auth.login'))

    return render_template('esqueci_senha.html')


@auth_bp.route('/reset-senha/<token>', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def reset_senha(token):
    """Página de redefinição de senha com token"""
    s = get_serializer()

    try:
        # Token válido por 1 hora (3600 segundos)
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('O link de recuperação expirou. Solicite um novo.', 'danger')
        return redirect(url_for('auth.esqueci_senha'))
    except BadSignature:
        flash('Link de recuperação inválido.', 'danger')
        return redirect(url_for('auth.esqueci_senha'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        senha = request.form.get('senha', '')
        senha_confirmacao = request.form.get('senha_confirmacao', '')

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('reset_senha.html', token=token)

        if senha != senha_confirmacao:
            flash('As senhas não coincidem.', 'warning')
            return render_template('reset_senha.html', token=token)

        user.set_senha(senha)
        db.session.commit()

        current_app.logger.info(f"Senha redefinida para: {email}")
        flash('Senha alterada com sucesso! Faça login com sua nova senha.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_senha.html', token=token)