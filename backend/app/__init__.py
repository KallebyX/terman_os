from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from celery import Celery
from config import Config

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
celery = Celery()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CORS(app)
    
    # Configurar Celery
    celery.conf.update(app.config)
    
    # Configurar login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    
    with app.app_context():
        # Importar e registrar blueprints
        from app.auth import bp as auth_bp
        from app.admin import bp as admin_bp
        from app.client import bp as client_bp
        from app.pdv import bp as pdv_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        app.register_blueprint(client_bp, url_prefix='/api/client')
        app.register_blueprint(pdv_bp, url_prefix='/api/pdv')
        
        # Criar tabelas
        db.create_all()
        
        return app

@login_manager.user_loader
def load_user(user_id):
    from .models.user import User
    return User.query.get(int(user_id)) 