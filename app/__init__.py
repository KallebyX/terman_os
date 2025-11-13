from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    if os.getenv('FLASK_ENV') == 'production':
        app.config['DEBUG'] = False
    else:
        app.config['DEBUG'] = True
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    login_manager.login_message = "Você precisa estar logado para acessar essa página."
    login_manager.login_message_category = "warning"

    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.marketplace import marketplace_bp
    from .routes.conteudo import conteudo_bp
    from .routes.site import site_bp
    from .routes.cliente import cliente_bp
    from .routes.dashboard import dashboard_bp

    app.register_blueprint(cliente_bp, url_prefix='/painel')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(marketplace_bp, url_prefix='/loja')
    app.register_blueprint(conteudo_bp, url_prefix='/conteudo')
    app.register_blueprint(site_bp)

    from .models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app