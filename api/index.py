"""
Vercel Serverless Function Entry Point
Este arquivo serve como ponto de entrada para a Vercel executar a aplicação Flask
"""
import os
import sys

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import redirect, jsonify, request
from app import create_app, db

# Criar aplicação Flask
app = create_app()

# Rota principal que redireciona para admin
@app.route('/')
def home():
    return redirect('/admin/')

# Inicializar banco de dados sob demanda (lazy initialization)
_db_initialized = False
_initial_data_created = False

def init_db():
    """Inicializa o banco de dados apenas uma vez por instância"""
    global _db_initialized
    if not _db_initialized:
        with app.app_context():
            try:
                db.create_all()
                _db_initialized = True
            except Exception as e:
                app.logger.warning(f"Não foi possível criar tabelas: {e}")

def create_initial_data_if_needed():
    """Cria dados iniciais automaticamente se o banco estiver vazio"""
    global _initial_data_created
    if _initial_data_created:
        return

    try:
        from app.models import User, Categoria
        from werkzeug.security import generate_password_hash

        # Verificar se já existe algum usuário
        user_count = User.query.count()

        if user_count == 0:
            app.logger.info("Banco vazio - criando dados iniciais...")

            # Criar Super Admin
            super_admin = User(
                nome="Kalleby Evangelho",
                email="kallebyevangelho03@gmail.com",
                senha_hash=generate_password_hash("kk030904K.k"),
                tipo_usuario="super_admin",
                ativo=True
            )
            db.session.add(super_admin)

            # Criar Admin padrão
            admin = User(
                nome="Administrador",
                email="admin@terman.com",
                senha_hash=generate_password_hash("admin123"),
                tipo_usuario="admin",
                ativo=True
            )
            db.session.add(admin)

            db.session.commit()
            app.logger.info("Usuários iniciais criados com sucesso!")

        # Verificar categorias
        if Categoria.query.count() == 0:
            categorias_padrao = [
                "Mangueiras Hidráulicas",
                "Mangueiras Industriais",
                "Conexões",
                "Ferramentas",
                "Acessórios"
            ]
            for nome in categorias_padrao:
                cat = Categoria(nome=nome)
                db.session.add(cat)
            db.session.commit()
            app.logger.info("Categorias padrão criadas!")

        _initial_data_created = True

    except Exception as e:
        app.logger.warning(f"Erro ao criar dados iniciais: {e}")
        db.session.rollback()

# Hook before_request para garantir que DB está inicializado
@app.before_request
def ensure_db():
    init_db()
    create_initial_data_if_needed()

# Endpoint de diagnóstico e inicialização manual
@app.route('/api/init-db')
def api_init_db():
    """
    Endpoint para inicializar/verificar o banco de dados.
    Acesse: https://seu-site.vercel.app/api/init-db
    """
    try:
        from app.models import User, Categoria
        from werkzeug.security import generate_password_hash

        results = {
            "status": "ok",
            "database": "connected",
            "tables_created": False,
            "users_created": [],
            "categories_created": False,
            "existing_users": []
        }

        # Criar tabelas
        db.create_all()
        results["tables_created"] = True

        # Verificar usuários existentes
        existing_users = User.query.all()
        results["existing_users"] = [
            {"email": u.email, "tipo": u.tipo_usuario, "ativo": u.ativo}
            for u in existing_users
        ]

        # Criar Super Admin se não existir
        super_admin_email = 'kallebyevangelho03@gmail.com'
        super_admin = User.query.filter_by(email=super_admin_email).first()

        if not super_admin:
            super_admin = User(
                nome="Kalleby Evangelho",
                email=super_admin_email,
                senha_hash=generate_password_hash("kk030904K.k"),
                tipo_usuario="super_admin",
                ativo=True
            )
            db.session.add(super_admin)
            results["users_created"].append(super_admin_email)
        elif super_admin.tipo_usuario != 'super_admin' or not super_admin.ativo:
            super_admin.tipo_usuario = 'super_admin'
            super_admin.ativo = True
            results["users_created"].append(f"{super_admin_email} (atualizado)")

        # Criar Admin se não existir
        admin_email = 'admin@terman.com'
        admin = User.query.filter_by(email=admin_email).first()

        if not admin:
            admin = User(
                nome="Administrador",
                email=admin_email,
                senha_hash=generate_password_hash("admin123"),
                tipo_usuario="admin",
                ativo=True
            )
            db.session.add(admin)
            results["users_created"].append(admin_email)

        # Criar categorias se não existirem
        if Categoria.query.count() == 0:
            categorias_padrao = [
                "Mangueiras Hidráulicas",
                "Mangueiras Industriais",
                "Conexões",
                "Ferramentas",
                "Acessórios"
            ]
            for nome in categorias_padrao:
                cat = Categoria(nome=nome)
                db.session.add(cat)
            results["categories_created"] = True

        db.session.commit()

        # Atualizar lista de usuários
        all_users = User.query.all()
        results["all_users_after"] = [
            {"email": u.email, "tipo": u.tipo_usuario, "ativo": u.ativo}
            for u in all_users
        ]

        results["message"] = "Banco de dados inicializado com sucesso!"
        results["credentials"] = {
            "super_admin": {"email": "kallebyevangelho03@gmail.com", "senha": "kk030904K.k"},
            "admin": {"email": "admin@terman.com", "senha": "admin123"}
        }

        return jsonify(results)

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__
        }), 500

# Endpoint para verificar status do banco
@app.route('/api/db-status')
def api_db_status():
    """Verifica o status atual do banco de dados"""
    try:
        from app.models import User, Categoria, Produto

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {
                "users": User.query.count(),
                "categories": Categoria.query.count(),
                "products": Produto.query.count()
            },
            "users": [
                {"email": u.email, "tipo": u.tipo_usuario, "ativo": u.ativo}
                for u in User.query.all()
            ]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# Exportar app para Vercel (WSGI compatível)
# Vercel detecta automaticamente o objeto 'app' ou 'application'
application = app
