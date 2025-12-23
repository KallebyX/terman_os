from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(512), nullable=False)
    tipo_usuario = db.Column(db.String(20), default='cliente')  # 'super_admin', 'admin' ou 'cliente'
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime, nullable=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_super_admin(self):
        """Verifica se o usuario e super admin"""
        return self.tipo_usuario == 'super_admin'

    def is_admin(self):
        """Verifica se o usuario e admin ou super admin"""
        return self.tipo_usuario in ['admin', 'super_admin']

    def pode_gerenciar_usuarios(self):
        """Apenas super admin pode gerenciar usuarios"""
        return self.tipo_usuario == 'super_admin'

    def __repr__(self):
        return f'<User {self.email}>'