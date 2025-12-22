import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

def get_database_url():
    """
    Obtém a URL do banco de dados, corrigindo o protocolo se necessário.
    Vercel/Render usam postgres:// mas SQLAlchemy requer postgresql://
    """
    database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')

    # Corrigir postgres:// para postgresql:// (Heroku, Render, etc)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    return database_url


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'segredo_padrao_mude_em_producao')
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Vercel/Serverless detection
    IS_VERCEL = os.getenv('VERCEL', False)
    IS_SERVERLESS = IS_VERCEL or os.getenv('AWS_LAMBDA_FUNCTION_NAME', False)

    # Diretório de upload de imagens
    # Em produção Vercel, use serviços externos como S3, Cloudinary, etc.
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join('app', 'static', 'produtos'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # URL base para imagens (Cloudinary, S3, etc)
    IMAGES_BASE_URL = os.getenv('IMAGES_BASE_URL', '/static/produtos/')

    # Rate Limiting
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True') == 'True'
    RATELIMIT_STORAGE_URI = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "200 per day;50 per hour"

    # Email Configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@terman.com')

    # Cache Configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    CACHE_REDIS_URL = os.getenv('REDIS_URL')

    # Logging - Em produção/Vercel, sempre use stdout
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'True') == 'True'  # Default True para Vercel

    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # CSRF Protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour