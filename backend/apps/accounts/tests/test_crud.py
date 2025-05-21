from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCRUDTests(TestCase):
    """
    Testes para operações CRUD de usuários.
    """
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register')
        self.users_url = reverse('accounts:users-list')
        self.profile_url = reverse('accounts:me')
        
        # Criar usuário admin
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        
        # Dados para criar um novo usuário
        self.new_user_data = {
            'email': 'newuser@example.com',
            'password': 'NewUserPassword123',
            'password_confirmation': 'NewUserPassword123',
            'first_name': 'New',
            'last_name': 'User'
        }

    def test_create_user(self):
        """Teste de criação de usuário."""
        response = self.client.post(self.register_url, self.new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        
    def test_read_user(self):
        """Teste de leitura de usuário."""
        # Criar usuário primeiro
        user = User.objects.create_user(
            email='readtest@example.com',
            password='ReadTestPassword123',
            first_name='Read',
            last_name='Test'
        )
        
        # Admin pode ler qualquer usuário
        self.client.force_authenticate(user=self.admin)
        url = reverse('accounts:users-detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'readtest@example.com')
        
        # Usuário pode ler seu próprio perfil
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'readtest@example.com')
        
    def test_update_user(self):
        """Teste de atualização de usuário."""
        # Criar usuário primeiro
        user = User.objects.create_user(
            email='updatetest@example.com',
            password='UpdateTestPassword123',
            first_name='Update',
            last_name='Test'
        )
        
        # Usuário pode atualizar seu próprio perfil
        self.client.force_authenticate(user=user)
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'phone': '123456789',
                'city': 'Test City',
                'state': 'TS'
            }
        }
        response = self.client.patch(self.profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.last_name, 'Name')
        self.assertEqual(user.profile.phone, '123456789')
        self.assertEqual(user.profile.city, 'Test City')
        self.assertEqual(user.profile.state, 'TS')
        
    def test_delete_user(self):
        """Teste de exclusão de usuário."""
        # Criar usuário primeiro
        user = User.objects.create_user(
            email='deletetest@example.com',
            password='DeleteTestPassword123',
            first_name='Delete',
            last_name='Test'
        )
        
        # Admin pode excluir usuário
        self.client.force_authenticate(user=self.admin)
        url = reverse('accounts:users-detail', args=[user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email='deletetest@example.com').exists())
