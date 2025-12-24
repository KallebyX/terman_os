"""
Rotas do Super Admin - Acesso total ao sistema
Gerenciamento completo de usuarios, configuracoes e todos os modulos
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.categoria import Categoria
from app import db
from app.decorators import super_admin_required
from datetime import datetime

super_admin_bp = Blueprint('super_admin', __name__)


# =============================================
# DASHBOARD SUPER ADMIN
# =============================================
@super_admin_bp.route('/')
@super_admin_bp.route('/dashboard')
@login_required
@super_admin_required
def dashboard():
    """Dashboard principal do Super Admin com visao geral do sistema"""
    # Inicializar variaveis com valores padrao
    total_usuarios = 0
    total_admins = 0
    total_clientes = 0
    total_super_admins = 0
    usuarios_ativos = 0
    usuarios_inativos = 0
    total_produtos = 0
    total_pedidos = 0
    total_categorias = 0
    ultimos_usuarios = []

    try:
        # Estatisticas de usuarios
        total_usuarios = User.query.count()
        total_admins = User.query.filter_by(tipo_usuario='admin').count()
        total_clientes = User.query.filter_by(tipo_usuario='cliente').count()
        total_super_admins = User.query.filter_by(tipo_usuario='super_admin').count()

        try:
            usuarios_ativos = User.query.filter_by(ativo=True).count()
            usuarios_inativos = User.query.filter_by(ativo=False).count()
        except Exception as e:
            current_app.logger.warning(f'Erro ao contar usuarios ativos/inativos: {e}')
            usuarios_ativos = total_usuarios
            usuarios_inativos = 0

        # Ultimos usuarios
        try:
            ultimos_usuarios = User.query.order_by(User.data_criacao.desc()).limit(5).all()
        except Exception as e:
            current_app.logger.warning(f'Erro ao buscar ultimos usuarios: {e}')
            try:
                ultimos_usuarios = User.query.order_by(User.id.desc()).limit(5).all()
            except Exception:
                ultimos_usuarios = []

    except Exception as e:
        current_app.logger.error(f'Erro ao carregar estatisticas de usuarios: {e}')

    # Estatisticas de produtos
    try:
        total_produtos = Produto.query.count()
    except Exception as e:
        current_app.logger.warning(f'Erro ao contar produtos: {e}')

    # Estatisticas de pedidos
    try:
        total_pedidos = Pedido.query.count()
    except Exception as e:
        current_app.logger.warning(f'Erro ao contar pedidos: {e}')

    # Estatisticas de categorias
    try:
        total_categorias = Categoria.query.count()
    except Exception as e:
        current_app.logger.warning(f'Erro ao contar categorias: {e}')

    return render_template('super_admin/dashboard.html',
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_clientes=total_clientes,
        total_super_admins=total_super_admins,
        usuarios_ativos=usuarios_ativos,
        usuarios_inativos=usuarios_inativos,
        total_produtos=total_produtos,
        total_pedidos=total_pedidos,
        total_categorias=total_categorias,
        ultimos_usuarios=ultimos_usuarios
    )


# =============================================
# CRUD COMPLETO DE USUARIOS
# =============================================
@super_admin_bp.route('/usuarios')
@login_required
@super_admin_required
def listar_usuarios():
    """Lista todos os usuarios do sistema"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Filtros
    tipo_filtro = request.args.get('tipo', '')
    status_filtro = request.args.get('status', '')
    busca = request.args.get('busca', '')

    query = User.query

    if tipo_filtro:
        query = query.filter_by(tipo_usuario=tipo_filtro)

    if status_filtro == 'ativo':
        query = query.filter_by(ativo=True)
    elif status_filtro == 'inativo':
        query = query.filter_by(ativo=False)

    if busca:
        query = query.filter(
            (User.nome.ilike(f'%{busca}%')) |
            (User.email.ilike(f'%{busca}%'))
        )

    usuarios = query.order_by(User.data_criacao.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('super_admin/usuarios/listar.html',
        usuarios=usuarios,
        tipo_filtro=tipo_filtro,
        status_filtro=status_filtro,
        busca=busca
    )


@super_admin_bp.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
@super_admin_required
def novo_usuario():
    """Criar novo usuario"""
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        tipo_usuario = request.form.get('tipo_usuario', 'cliente')
        ativo = request.form.get('ativo') == 'on'

        # Validacoes
        if not nome or not email or not senha:
            flash('Preencha todos os campos obrigatorios.', 'warning')
            return render_template('super_admin/usuarios/novo.html')

        if len(senha) < 6:
            flash('A senha deve ter pelo menos 6 caracteres.', 'warning')
            return render_template('super_admin/usuarios/novo.html')

        if User.query.filter_by(email=email).first():
            flash('Este email ja esta cadastrado.', 'warning')
            return render_template('super_admin/usuarios/novo.html')

        # Validar tipo de usuario
        if tipo_usuario not in ['cliente', 'admin', 'super_admin']:
            tipo_usuario = 'cliente'

        try:
            novo = User(
                nome=nome,
                email=email,
                tipo_usuario=tipo_usuario,
                ativo=ativo
            )
            novo.set_senha(senha)
            db.session.add(novo)
            db.session.commit()

            current_app.logger.info(f'Super Admin {current_user.email} criou usuario: {email}')
            flash(f'Usuario {nome} criado com sucesso!', 'success')
            return redirect(url_for('super_admin.listar_usuarios'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao criar usuario: {e}')
            flash('Erro ao criar usuario. Tente novamente.', 'danger')

    return render_template('super_admin/usuarios/novo.html')


@super_admin_bp.route('/usuarios/<int:user_id>')
@login_required
@super_admin_required
def visualizar_usuario(user_id):
    """Ver detalhes de um usuario"""
    usuario = User.query.get_or_404(user_id)
    return render_template('super_admin/usuarios/visualizar.html', usuario=usuario)


@super_admin_bp.route('/usuarios/<int:user_id>/editar', methods=['GET', 'POST'])
@login_required
@super_admin_required
def editar_usuario(user_id):
    """Editar usuario existente"""
    usuario = User.query.get_or_404(user_id)

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        tipo_usuario = request.form.get('tipo_usuario', usuario.tipo_usuario)
        ativo = request.form.get('ativo') == 'on'
        nova_senha = request.form.get('nova_senha', '').strip()

        # Validacoes
        if not nome or not email:
            flash('Nome e email sao obrigatorios.', 'warning')
            return render_template('super_admin/usuarios/editar.html', usuario=usuario)

        # Verificar se email ja existe (outro usuario)
        outro = User.query.filter_by(email=email).first()
        if outro and outro.id != user_id:
            flash('Este email ja esta sendo usado por outro usuario.', 'warning')
            return render_template('super_admin/usuarios/editar.html', usuario=usuario)

        # Validar tipo de usuario
        if tipo_usuario not in ['cliente', 'admin', 'super_admin']:
            tipo_usuario = usuario.tipo_usuario

        try:
            usuario.nome = nome
            usuario.email = email
            usuario.tipo_usuario = tipo_usuario
            usuario.ativo = ativo

            if nova_senha:
                if len(nova_senha) < 6:
                    flash('A nova senha deve ter pelo menos 6 caracteres.', 'warning')
                    return render_template('super_admin/usuarios/editar.html', usuario=usuario)
                usuario.set_senha(nova_senha)

            db.session.commit()

            current_app.logger.info(f'Super Admin {current_user.email} editou usuario: {email}')
            flash(f'Usuario {nome} atualizado com sucesso!', 'success')
            return redirect(url_for('super_admin.listar_usuarios'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Erro ao editar usuario: {e}')
            flash('Erro ao atualizar usuario. Tente novamente.', 'danger')

    return render_template('super_admin/usuarios/editar.html', usuario=usuario)


@super_admin_bp.route('/usuarios/<int:user_id>/excluir', methods=['POST'])
@login_required
@super_admin_required
def excluir_usuario(user_id):
    """Excluir usuario do sistema"""
    usuario = User.query.get_or_404(user_id)

    # Nao permitir excluir a si mesmo
    if usuario.id == current_user.id:
        flash('Voce nao pode excluir sua propria conta.', 'danger')
        return redirect(url_for('super_admin.listar_usuarios'))

    try:
        email = usuario.email
        db.session.delete(usuario)
        db.session.commit()

        current_app.logger.info(f'Super Admin {current_user.email} excluiu usuario: {email}')
        flash(f'Usuario {email} excluido com sucesso!', 'info')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao excluir usuario: {e}')
        flash('Erro ao excluir usuario. Tente novamente.', 'danger')

    return redirect(url_for('super_admin.listar_usuarios'))


@super_admin_bp.route('/usuarios/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@super_admin_required
def toggle_status_usuario(user_id):
    """Ativar/Desativar usuario"""
    usuario = User.query.get_or_404(user_id)

    # Nao permitir desativar a si mesmo
    if usuario.id == current_user.id:
        flash('Voce nao pode desativar sua propria conta.', 'danger')
        return redirect(url_for('super_admin.listar_usuarios'))

    try:
        usuario.ativo = not usuario.ativo
        db.session.commit()

        status = 'ativado' if usuario.ativo else 'desativado'
        current_app.logger.info(f'Super Admin {current_user.email} {status} usuario: {usuario.email}')
        flash(f'Usuario {usuario.nome} {status} com sucesso!', 'success')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao alterar status do usuario: {e}')
        flash('Erro ao alterar status. Tente novamente.', 'danger')

    return redirect(url_for('super_admin.listar_usuarios'))


@super_admin_bp.route('/usuarios/<int:user_id>/reset-senha', methods=['POST'])
@login_required
@super_admin_required
def reset_senha_usuario(user_id):
    """Resetar senha do usuario para uma senha temporaria"""
    usuario = User.query.get_or_404(user_id)

    nova_senha = request.form.get('nova_senha', '').strip()

    if not nova_senha or len(nova_senha) < 6:
        flash('A nova senha deve ter pelo menos 6 caracteres.', 'warning')
        return redirect(url_for('super_admin.editar_usuario', user_id=user_id))

    try:
        usuario.set_senha(nova_senha)
        db.session.commit()

        current_app.logger.info(f'Super Admin {current_user.email} resetou senha de: {usuario.email}')
        flash(f'Senha do usuario {usuario.nome} alterada com sucesso!', 'success')

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Erro ao resetar senha: {e}')
        flash('Erro ao resetar senha. Tente novamente.', 'danger')

    return redirect(url_for('super_admin.listar_usuarios'))


# =============================================
# CONFIGURACOES DO SISTEMA
# =============================================
@super_admin_bp.route('/configuracoes')
@login_required
@super_admin_required
def configuracoes():
    """Pagina de configuracoes do sistema"""
    return render_template('super_admin/configuracoes.html')


# =============================================
# LOGS E AUDITORIA
# =============================================
@super_admin_bp.route('/logs')
@login_required
@super_admin_required
def logs_sistema():
    """Visualizar logs do sistema"""
    return render_template('super_admin/logs.html')


# =============================================
# API ENDPOINTS PARA AJAX
# =============================================
@super_admin_bp.route('/api/usuarios/stats')
@login_required
@super_admin_required
def api_usuarios_stats():
    """Retorna estatisticas de usuarios em JSON"""
    stats = {
        'total': User.query.count(),
        'ativos': User.query.filter_by(ativo=True).count(),
        'inativos': User.query.filter_by(ativo=False).count(),
        'por_tipo': {
            'super_admin': User.query.filter_by(tipo_usuario='super_admin').count(),
            'admin': User.query.filter_by(tipo_usuario='admin').count(),
            'cliente': User.query.filter_by(tipo_usuario='cliente').count()
        }
    }
    return jsonify(stats)
