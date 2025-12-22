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

# Criar tabelas do banco de dados na primeira execução
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        app.logger.warning(f"Não foi possível criar tabelas: {e}")

# Handler para Vercel
def handler(request, context):
    """Handler para Vercel serverless functions"""
    return app(request.environ, context)

# Para compatibilidade com Vercel
application = app
