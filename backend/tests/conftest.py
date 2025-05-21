import os
import pytest
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caminho_correto_do_seu_projeto.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
def get_jwt_token():
    def _get_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    return _get_jwt_token
