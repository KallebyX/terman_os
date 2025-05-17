import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'segredo_padrao')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Diretório de upload de imagens
    UPLOAD_FOLDER = os.path.join('app', 'static', 'produtos')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de 16MB para uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}