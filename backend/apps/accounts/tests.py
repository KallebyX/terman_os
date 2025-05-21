from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserModelTests(TestCase):
    """
    Testes para o modelo User.
    """
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'user_type': 'admin'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Teste de criação de usuário."""
        self.assertEqual(self.user.email, self.user_data['email'])
        self.assertEqual(self.user.first_name, self.user_data['first_name'])
        self.assertEqual(self.user.last_name, self.user_data['last_name'])
        self.assertEqual(self.user.user_type, self.user_data['user_type'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        """Teste de criação de superusuário."""
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPassword123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.user_type, 'admin')

    def test_user_profile_creation(self):
        """Teste de criação automática de perfil."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_user_str_representation(self):
        """Teste da representação string do usuário."""
        expected_str = f"{self.user.get_full_name()} ({self.user.email})"
        self.assertEqual(str(self.user), expected_str)

    def test_user_full_name(self):
        """Teste do método get_full_name."""
        expected_full_name = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(self.user.get_full_name(), expected_full_name)

    def test_user_short_name(self):
        """Teste do método get_short_name."""
        self.assertEqual(self.user.get_short_name(), self.user.first_name)

    def test_user_type_properties(self):
        """Teste das propriedades de tipo de usuário."""
        self.assertTrue(self.user.is_admin)
        self.assertFalse(self.user.is_seller)
        self.assertFalse(self.user.is_operator)
        self.assertFalse(self.user.is_customer)

        self.user.user_type = 'seller'
        self.user.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_admin)
        self.assertTrue(self.user.is_seller)
        self.assertFalse(self.user.is_operator)
        self.assertFalse(self.user.is_customer)


class UserAPITests(TestCase):
    """
    Testes para as APIs de usuário.
    """
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User'
        )
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='UserPassword123',
            first_name='Regular',
            last_name='User',
            user_type='customer'
        )
        self.seller_user = User.objects.create_user(
            email='seller@example.com',
            password='SellerPassword123',
            first_name='Seller',
            last_name='User',
            user_type='seller'
        )
        self.operator_user = User.objects.create_user(
            email='operator@example.com',
            password='OperatorPassword123',
            first_name='Operator',
            last_name='User',
            user_type='operator'
        )

    def test_user_registration(self):
        """Teste de registro de usuário."""
        url = reverse('accounts:register')
        data = {
            'email': 'newuser@example.com',
            'password': 'NewUserPassword123',
            'password_confirmation': 'NewUserPassword123',
            'first_name': 'New',
            'last_name': 'User',
            'user_type': 'customer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login(self):
        """Teste de login de usuário."""
        url = reverse('accounts:login')
        data = {
            'email': 'user@example.com',
            'password': 'UserPassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_profile(self):
        """Teste de acesso ao perfil do usuário."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('accounts:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.regular_user.email)
        self.assertEqual(response.data['first_name'], self.regular_user.first_name)
        self.assertEqual(response.data['last_name'], self.regular_user.last_name)
        self.assertEqual(response.data['user_type'], self.regular_user.user_type)

    def test_user_profile_update(self):
        """Teste de atualização do perfil do usuário."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('accounts:me')
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'phone': '123456789',
                'city': 'Test City',
                'state': 'TS'
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertEqual(self.regular_user.first_name, 'Updated')
        self.assertEqual(self.regular_user.last_name, 'Name')
        self.assertEqual(self.regular_user.profile.phone, '123456789')
        self.assertEqual(self.regular_user.profile.city, 'Test City')
        self.assertEqual(self.regular_user.profile.state, 'TS')

    def test_admin_can_view_all_users(self):
        """Teste de que administradores podem ver todos os usuários."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('accounts:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)  # 4 usuários criados no setUp

    def test_regular_user_can_only_view_self(self):
        """Teste de que usuários comuns só podem ver a si mesmos."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('accounts:users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Apenas o próprio usuário
        self.assertEqual(response.data['results'][0]['id'], self.regular_user.id)

    def test_user_permissions(self):
        """Teste de permissões de usuário."""
        # Usuário não autenticado não pode acessar perfil
        url = reverse('accounts:me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Usuário comum não pode acessar detalhes de outro usuário
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('accounts:users-detail', args=[self.seller_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Admin pode acessar detalhes de qualquer usuário
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.seller_user.id)
