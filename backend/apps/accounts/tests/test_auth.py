from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class JWTAuthenticationTests(TestCase):
    """
    Testes para autenticação JWT.
    """
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:me')
        
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'password_confirmation': 'TestPassword123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        self.login_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123'
        }

    def test_user_registration_returns_jwt(self):
        """Teste se o registro retorna tokens JWT."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_login_returns_jwt(self):
        """Teste se o login retorna tokens JWT."""
        # Criar usuário primeiro
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        
        # Fazer login
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_protected_route_requires_jwt(self):
        """Teste se rotas protegidas requerem JWT."""
        # Tentar acessar perfil sem autenticação
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Criar usuário e fazer login
        User.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name']
        )
        
        login_response = self.client.post(self.login_url, self.login_data, format='json')
        access_token = login_response.data['access']
        
        # Acessar perfil com token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_expired_token_is_rejected(self):
        """Teste se tokens expirados são rejeitados."""
        # Este é um token JWT expirado (apenas para teste)
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjE5NzE2ODAwLCJpYXQiOjE2MTk3MTY4MDAsImp0aSI6ImY1NjU3NzVjOTM1ZDQ5OTc5OGY5ZGNmMzY4NGFhYTJjIiwidXNlcl9pZCI6MX0.XrCxIy-WGe1Bpl2Ea7A4tRlxS9-zx-qYgRlLAXUUkxQ"
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
