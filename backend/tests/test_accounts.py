import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email='user@example.com', password='UserPassword123', is_admin=False):
        # Verificar se o usuário já existe para evitar erros de duplicação
        try:
            user = User.objects.get(email=email)
            # Atualizar campos se necessário
            user.is_admin = is_admin
            user.set_password(password)
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name='Test',
                last_name='User',
                is_admin=is_admin
            )
        return user
    return _create_user

@pytest.mark.django_db
class TestUserAPI:
    def test_user_registration(self, api_client):
        """Teste de registro de usuário."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'NewUserPassword123',
            'password_confirmation': 'NewUserPassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newuser@example.com').exists()
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data

    def test_user_login(self, api_client, create_user):
        """Teste de login de usuário."""
        create_user()
        url = reverse('accounts:login')
        data = {
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data

    def test_user_profile(self, api_client, create_user, get_jwt_token):
        """Teste de acesso ao perfil do usuário."""
        user = create_user()
        # Autenticar usando JWT
        token = get_jwt_token(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('accounts:me')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert response.data['last_name'] == user.last_name

    def test_admin_can_view_all_users(self, api_client, create_user):
        """Teste de que administradores podem ver todos os usuários."""
        admin_user = create_user(email='admin@example.com', is_admin=True)
        create_user(email='user1@example.com')
        create_user(email='user2@example.com')
        
        api_client.force_authenticate(user=admin_user)
        url = reverse('accounts:users-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 3  # Pelo menos 3 usuários criados

    def test_regular_user_can_only_view_self(self, api_client, create_user):
        """Teste de que usuários comuns só podem ver a si mesmos."""
        user = create_user()
        create_user(email='other@example.com')
        
        api_client.force_authenticate(user=user)
        url = reverse('accounts:users-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1  # Apenas o próprio usuário
        assert response.data['results'][0]['id'] == user.id
        
    def test_token_refresh(self, api_client, create_user):
        """Teste de renovação do token JWT."""
        create_user()
        # Primeiro, fazer login para obter o token de atualização
        login_url = reverse('accounts:login')
        login_data = {
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }
        login_response = api_client.post(login_url, login_data, format='json')
        assert login_response.status_code == status.HTTP_200_OK
        
        # Usar o token de atualização para obter um novo token de acesso
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': login_response.data['refresh']
        }
        refresh_response = api_client.post(refresh_url, refresh_data, format='json')
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
        
    def test_token_verify(self, api_client, create_user):
        """Teste de verificação do token JWT."""
        create_user()
        # Primeiro, fazer login para obter o token
        login_url = reverse('accounts:login')
        login_data = {
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }
        login_response = api_client.post(login_url, login_data, format='json')
        assert login_response.status_code == status.HTTP_200_OK
        
        # Verificar o token de acesso
        verify_url = reverse('token_verify')
        verify_data = {
            'token': login_response.data['access']
        }
        verify_response = api_client.post(verify_url, verify_data, format='json')
        assert verify_response.status_code == status.HTTP_200_OK
