"""
Vercel Serverless Function Entry Point
Este arquivo serve como ponto de entrada para a Vercel executar a aplicação Flask
"""
import os
import sys

# Adicionar o diretório raiz ao path do Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import redirect
from app import create_app, db

# Criar aplicação Flask
app = create_app()

# Rota principal que redireciona para admin
@app.route('/')
def home():
    return redirect('/admin/')

# Inicializar banco de dados sob demanda (lazy initialization)
_db_initialized = False

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

# Hook before_request para garantir que DB está inicializado
@app.before_request
def ensure_db():
    init_db()

# Exportar app para Vercel (WSGI compatível)
# Vercel detecta automaticamente o objeto 'app' ou 'application'
application = app
