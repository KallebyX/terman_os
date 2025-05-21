import os
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nome_do_seu_projeto.settings')
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def get_jwt_token():
    def _get_jwt_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    return _get_jwt_token
