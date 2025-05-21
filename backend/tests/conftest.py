import os
import django
import pytest

# Configurar Django antes de importar cualquier módulo que dependa de la configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar después de configurar Django
from rest_framework_simplejwt.tokens import RefreshToken

def get_jwt_token():
    def _get_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    return _get_jwt_token