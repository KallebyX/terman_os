import os
import django
import pytest
from django.conf import settings

# Configurar Django antes de importar qualquer módulo que dependa da configuração
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar depois de configurar Django
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    return _get_jwt_token

@pytest.fixture
def authenticated_client():
    def _authenticated_client(user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
        return client
    return _authenticated_client

# Configuração para usar o banco de dados de teste
@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
