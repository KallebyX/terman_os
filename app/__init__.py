from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_caching import Cache
import os
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
limiter = Limiter(key_func=get_remote_address)
mail = Mail()
cache = Cache()

def create_app():
    app = Flask(__name__)
    if os.getenv('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True
    app.config.from_object('config.Config')

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    limiter.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Configurar logging
    setup_logging(app)

    login_manager.login_message = "Você precisa estar logado para acessar essa página."
    login_manager.login_message_category = "warning"

    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.marketplace import marketplace_bp
    from .routes.conteudo import conteudo_bp
    from .routes.site import site_bp
    from .routes.cliente import cliente_bp
    from .routes.dashboard import dashboard_bp
    from .routes.crm import crm_bp
    from .routes.erp import erp_bp

    app.register_blueprint(cliente_bp, url_prefix='/painel')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(marketplace_bp, url_prefix='/loja')
    app.register_blueprint(conteudo_bp, url_prefix='/conteudo')
    app.register_blueprint(site_bp)
    app.register_blueprint(crm_bp, url_prefix='/crm')
    app.register_blueprint(erp_bp, url_prefix='/erp')

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registrar error handlers
    register_error_handlers(app)

    return app


def setup_logging(app):
    """Configurar sistema de logging"""
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)

    # Formato de log
    log_format = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )

    # Sempre adicionar handler para stdout (necessário para Vercel, Render, etc)
    if app.config.get('LOG_TO_STDOUT', True):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(log_level)
        app.logger.addHandler(stream_handler)

    # Adicionar file handler apenas se não for produção/serverless
    if not app.debug and not app.testing and not app.config.get('LOG_TO_STDOUT', True):
        try:
            if not os.path.exists('logs'):
                os.mkdir('logs')

            file_handler = RotatingFileHandler(
                'logs/terman_os.log',
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(log_format)
            file_handler.setLevel(log_level)
            app.logger.addHandler(file_handler)
        except Exception as e:
            app.logger.warning(f'Não foi possível criar logs em arquivo: {e}')

    app.logger.setLevel(log_level)
    app.logger.info('Terman OS inicializado')


def register_error_handlers(app):
    """Registrar handlers de erro personalizados"""
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f'Página não encontrada: {error}')
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Erro interno: {error}')
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.warning(f'Acesso negado: {error}')
        return render_template('errors/403.html'), 403