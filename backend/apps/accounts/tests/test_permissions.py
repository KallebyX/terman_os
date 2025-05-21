from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class PermissionsTests(TestCase):
    """
    Testes para permissões de usuário.
    """
    def setUp(self):
        self.client = APIClient()
        self.users_url = reverse('accounts:users-list')
        
        # Criar usuários de diferentes tipos
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        
        self.seller = User.objects.create_user(
            email='seller@example.com',
            password='SellerPassword123',
            first_name='Seller',
            last_name='User',
            is_seller=True
        )
        
        self.operator = User.objects.create_user(
            email='operator@example.com',
            password='OperatorPassword123',
            first_name='Operator',
            last_name='User',
            is_operator=True
        )
        
        self.customer = User.objects.create_user(
            email='customer@example.com',
            password='CustomerPassword123',
            first_name='Customer',
            last_name='User'
        )

    def test_admin_can_list_all_users(self):
        """Teste se administradores podem listar todos os usuários."""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)  # 4 usuários criados no setUp
        
    def test_non_admin_can_only_see_self(self):
        """Teste se usuários não-admin só podem ver a si mesmos."""
        # Testar com vendedor
        self.client.force_authenticate(user=self.seller)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.seller.id)
        
        # Testar com operador
        self.client.force_authenticate(user=self.operator)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.operator.id)
        
        # Testar com cliente
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id'], self.customer.id)
        
    def test_admin_can_update_any_user(self):
        """Teste se administradores podem atualizar qualquer usuário."""
        self.client.force_authenticate(user=self.admin)
        url = reverse('accounts:users-detail', args=[self.customer.id])
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Updated')
        
    def test_non_admin_cannot_update_others(self):
        """Teste se usuários não-admin não podem atualizar outros usuários."""
        self.client.force_authenticate(user=self.seller)
        url = reverse('accounts:users-detail', args=[self.customer.id])
        data = {'first_name': 'Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.first_name, 'Customer')  # Não deve mudar
