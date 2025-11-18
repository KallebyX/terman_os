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
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@terman.com')

    # Cache Configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = os.getenv('REDIS_URL')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'False') == 'True'