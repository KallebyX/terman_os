from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Estoque, MovimentacaoEstoque
from apps.products.models import Produto, Categoria
from apps.accounts.models import User


class InventoryAPITests(TestCase):
    """
    Testes para as APIs de inventário.
    """
    def setUp(self):
        self.client = APIClient()
        
        # Criar usuários para testes
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User'
        )
        
        self.seller_user = User.objects.create_user(
            email='seller@example.com',
            password='SellerPassword123',
            first_name='Seller',
            last_name='User',
            user_type='seller'
        )
        
        self.customer_user = User.objects.create_user(
            email='customer@example.com',
            password='CustomerPassword123',
            first_name='Customer',
            last_name='User',
            user_type='customer'
        )
        
        # Criar categoria para testes
        self.categoria = Categoria.objects.create(
            nome='Mangueiras Hidráulicas',
            descricao='Mangueiras para sistemas hidráulicos',
            slug='mangueiras-hidraulicas',
            ativa=True
        )
        
        # Criar produtos para testes
        self.produto1 = Produto.objects.create(
            codigo='MH001',
            nome='Mangueira Hidráulica 1/2"',
            descricao='Mangueira hidráulica de alta pressão',
            preco=100.00,
            unidade='m',
            slug='mangueira-hidraulica-1-2',
            ativo=True,
            estoque_minimo=10.00
        )
        self.produto1.categorias.add(self.categoria)
        
        self.produto2 = Produto.objects.create(
            codigo='MH002',
            nome='Mangueira Hidráulica 3/4"',
            descricao='Mangueira hidráulica de alta pressão',
            preco=150.00,
            unidade='m',
            slug='mangueira-hidraulica-3-4',
            ativo=True,
            estoque_minimo=5.00
        )
        self.produto2.categorias.add(self.categoria)
        
        # Criar estoque para testes
        self.estoque1 = Estoque.objects.create(
            produto=self.produto1,
            quantidade_atual=20.00,
            quantidade_reservada=5.00
        )
        
        self.estoque2 = Estoque.objects.create(
            produto=self.produto2,
            quantidade_atual=3.00,
            quantidade_reservada=0.00
        )
        
        # Criar movimentações para testes
        self.movimentacao1 = MovimentacaoEstoque.objects.create(
            produto=self.produto1,
            tipo='entrada',
            origem='compra',
            quantidade=20.00,
            valor_unitario=90.00,
            documento='NF-001',
            observacao='Compra inicial',
            usuario=self.admin_user
        )
        
        self.movimentacao2 = MovimentacaoEstoque.objects.create(
            produto=self.produto1,
            tipo='saida',
            origem='venda',
            quantidade=5.00,
            valor_unitario=100.00,
            documento='PV-001',
            observacao='Venda para cliente',
            usuario=self.seller_user
        )

    def test_listar_estoque_com_admin(self):
        """Teste de listagem de estoque com admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:estoque-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_listar_estoque_com_vendedor(self):
        """Teste de listagem de estoque com vendedor."""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('inventory:estoque-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_listar_estoque_com_cliente(self):
        """Teste de listagem de estoque com cliente (não deve permitir)."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('inventory:estoque-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detalhar_estoque(self):
        """Teste de detalhamento de estoque."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:estoque-detail', kwargs={'pk': self.estoque1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['produto']['nome'], self.produto1.nome)
        self.assertEqual(float(response.data['quantidade_atual']), 20.00)
        self.assertEqual(float(response.data['quantidade_reservada']), 5.00)
        self.assertEqual(float(response.data['quantidade_disponivel']), 15.00)
        self.assertEqual(response.data['status'], 'normal')

    def test_listar_movimentacoes(self):
        """Teste de listagem de movimentações de estoque."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:movimentacoes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_ajuste_estoque_entrada(self):
        """Teste de ajuste de estoque (entrada)."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:ajuste-estoque')
        data = {
            'produto_id': self.produto1.id,
            'quantidade': 10.00,
            'tipo': 'entrada',
            'origem': 'compra',
            'documento': 'NF-002',
            'observacao': 'Compra adicional'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o estoque foi atualizado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_atual), 30.00)
        self.assertEqual(float(self.estoque1.quantidade_disponivel), 25.00)
        
        # Verificar se a movimentação foi registrada
        self.assertEqual(MovimentacaoEstoque.objects.count(), 3)
        movimentacao = MovimentacaoEstoque.objects.latest('data_movimentacao')
        self.assertEqual(movimentacao.produto, self.produto1)
        self.assertEqual(movimentacao.tipo, 'entrada')
        self.assertEqual(float(movimentacao.quantidade), 10.00)
        self.assertEqual(movimentacao.documento, 'NF-002')

    def test_ajuste_estoque_saida(self):
        """Teste de ajuste de estoque (saída)."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:ajuste-estoque')
        data = {
            'produto_id': self.produto1.id,
            'quantidade': 5.00,
            'tipo': 'saida',
            'origem': 'venda',
            'documento': 'PV-002',
            'observacao': 'Venda adicional'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o estoque foi atualizado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_atual), 15.00)
        self.assertEqual(float(self.estoque1.quantidade_disponivel), 10.00)
        
        # Verificar se a movimentação foi registrada
        self.assertEqual(MovimentacaoEstoque.objects.count(), 3)
        movimentacao = MovimentacaoEstoque.objects.latest('data_movimentacao')
        self.assertEqual(movimentacao.produto, self.produto1)
        self.assertEqual(movimentacao.tipo, 'saida')
        self.assertEqual(float(movimentacao.quantidade), 5.00)
        self.assertEqual(movimentacao.documento, 'PV-002')

    def test_ajuste_estoque_saida_insuficiente(self):
        """Teste de ajuste de estoque (saída) com quantidade insuficiente."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:ajuste-estoque')
        data = {
            'produto_id': self.produto1.id,
            'quantidade': 20.00,
            'tipo': 'saida',
            'origem': 'venda',
            'documento': 'PV-003',
            'observacao': 'Venda grande'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Quantidade insuficiente em estoque', response.data['detail'])
        
        # Verificar se o estoque não foi alterado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_atual), 20.00)
        
        # Verificar se nenhuma movimentação foi registrada
        self.assertEqual(MovimentacaoEstoque.objects.count(), 2)

    def test_produtos_baixo_estoque(self):
        """Teste de listagem de produtos com estoque baixo."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:produtos-baixo-estoque')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Apenas o produto2 está com estoque abaixo do mínimo
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['produto']['codigo'], self.produto2.codigo)
        self.assertEqual(response.data['results'][0]['status'], 'baixo')

    def test_relatorio_movimentacoes(self):
        """Teste de relatório de movimentações."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('inventory:relatorio-movimentacoes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['movimentacoes']), 2)
        self.assertEqual(float(response.data['total_entradas']), 20.00)
        self.assertEqual(float(response.data['total_saidas']), 5.00)
        self.assertEqual(float(response.data['saldo']), 15.00)
