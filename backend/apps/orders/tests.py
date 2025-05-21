from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.products.models import Produto, Categoria
from apps.inventory.models import Estoque, MovimentacaoEstoque
from .models import Order, OrderItem
from decimal import Decimal

User = get_user_model()


class OrderModelTests(TestCase):
    """
    Testes para o modelo Order.
    """
    def setUp(self):
        # Criar usuário
        self.user = User.objects.create_user(
            email='cliente@example.com',
            password='ClientePassword123',
            first_name='Cliente',
            last_name='Teste'
        )
        
        # Criar categoria
        self.categoria = Categoria.objects.create(nome='Teste')
        
        # Criar produtos
        self.produto1 = Produto.objects.create(
            nome='Produto 1',
            descricao='Descrição do produto 1',
            preco=100.00,
            categoria=self.categoria
        )
        
        self.produto2 = Produto.objects.create(
            nome='Produto 2',
            descricao='Descrição do produto 2',
            preco=200.00,
            categoria=self.categoria
        )
        
        # Criar estoques
        self.estoque1 = Estoque.objects.create(
            produto=self.produto1,
            quantidade_atual=10,
            quantidade_reservada=0
        )
        
        self.estoque2 = Estoque.objects.create(
            produto=self.produto2,
            quantidade_atual=5,
            quantidade_reservada=0
        )
        
        # Criar pedido
        self.order = Order.objects.create(
            customer=self.user,
            status='pending'
        )
    
    def test_add_item(self):
        """Teste de adição de item ao pedido."""
        # Adicionar item ao pedido
        item = self.order.add_item(self.produto1, 2)
        
        # Verificar se o item foi adicionado corretamente
        self.assertEqual(item.product, self.produto1)
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.price, self.produto1.preco)
        
        # Verificar se o total do pedido foi calculado corretamente
        self.assertEqual(self.order.subtotal, Decimal('200.00'))
        self.assertEqual(self.order.total, Decimal('200.00'))
        
        # Adicionar outro item
        item2 = self.order.add_item(self.produto2, 1)
        
        # Verificar se o total foi atualizado
        self.assertEqual(self.order.subtotal, Decimal('400.00'))
        self.assertEqual(self.order.total, Decimal('400.00'))
        
        # Adicionar mais unidades de um item existente
        item = self.order.add_item(self.produto1, 1)
        
        # Verificar se a quantidade foi atualizada
        self.assertEqual(item.quantity, 3)
        
        # Verificar se o total foi atualizado
        self.assertEqual(self.order.subtotal, Decimal('500.00'))
        self.assertEqual(self.order.total, Decimal('500.00'))
    
    def test_remove_item(self):
        """Teste de remoção de item do pedido."""
        # Adicionar itens ao pedido
        self.order.add_item(self.produto1, 2)
        self.order.add_item(self.produto2, 1)
        
        # Verificar total inicial
        self.assertEqual(self.order.subtotal, Decimal('400.00'))
        
        # Remover item
        result = self.order.remove_item(self.produto1)
        
        # Verificar se o item foi removido
        self.assertTrue(result)
        self.assertEqual(self.order.items.count(), 1)
        
        # Verificar se o total foi atualizado
        self.assertEqual(self.order.subtotal, Decimal('200.00'))
        
        # Tentar remover item inexistente
        result = self.order.remove_item(self.produto1)
        
        # Verificar que a operação falhou
        self.assertFalse(result)
    
    def test_update_item_quantity(self):
        """Teste de atualização de quantidade de item."""
        # Adicionar item ao pedido
        self.order.add_item(self.produto1, 2)
        
        # Atualizar quantidade
        result = self.order.update_item_quantity(self.produto1, 3)
        
        # Verificar se a quantidade foi atualizada
        self.assertTrue(result)
        item = self.order.items.get(product=self.produto1)
        self.assertEqual(item.quantity, 3)
        
        # Verificar se o total foi atualizado
        self.assertEqual(self.order.subtotal, Decimal('300.00'))
        
        # Atualizar quantidade para zero (deve remover o item)
        result = self.order.update_item_quantity(self.produto1, 0)
        
        # Verificar se o item foi removido
        self.assertTrue(result)
        self.assertEqual(self.order.items.count(), 0)
        
        # Tentar atualizar item inexistente
        result = self.order.update_item_quantity(self.produto1, 1)
        
        # Verificar que a operação falhou
        self.assertFalse(result)
    
    def test_order_flow(self):
        """Teste do fluxo completo de um pedido."""
        # Adicionar itens ao pedido
        self.order.add_item(self.produto1, 2)
        self.order.add_item(self.produto2, 1)
        
        # Definir informações de entrega
        self.order.shipping_address = 'Rua Teste, 123'
        self.order.shipping_city = 'Cidade Teste'
        self.order.shipping_state = 'ST'
        self.order.shipping_zip = '12345-678'
        self.order.save()
        
        # Finalizar pedido
        self.assertTrue(self.order.finalize_order())
        self.assertEqual(self.order.status, 'processing')
        
        # Registrar pagamento
        self.assertTrue(self.order.mark_as_paid('pix'))
        self.assertEqual(self.order.status, 'completed')
        self.assertEqual(self.order.payment_method, 'pix')
        self.assertIsNotNone(self.order.payment_date)
    
    def test_cancel_order(self):
        """Teste de cancelamento de pedido."""
        # Adicionar itens ao pedido
        self.order.add_item(self.produto1, 2)
        
        # Finalizar pedido
        self.order.shipping_address = 'Rua Teste, 123'
        self.order.shipping_city = 'Cidade Teste'
        self.order.shipping_state = 'ST'
        self.order.shipping_zip = '12345-678'
        self.order.finalize_order()
        
        # Cancelar pedido
        self.assertTrue(self.order.cancel())
        self.assertEqual(self.order.status, 'canceled')


class OrderAPITests(TestCase):
    """
    Testes para as APIs de pedido.
    """
    def setUp(self):
        # Criar usuários
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        
        self.seller_user = User.objects.create_user(
            email='seller@example.com',
            password='SellerPassword123',
            first_name='Seller',
            last_name='User',
            is_seller=True
        )
        
        self.customer_user = User.objects.create_user(
            email='customer@example.com',
            password='CustomerPassword123',
            first_name='Customer',
            last_name='User'
        )
        
        self.another_customer = User.objects.create_user(
            email='another@example.com',
            password='AnotherPassword123',
            first_name='Another',
            last_name='Customer'
        )
        
        # Criar categoria
        self.categoria = Categoria.objects.create(nome='Teste')
        
        # Criar produtos
        self.produto1 = Produto.objects.create(
            nome='Produto 1',
            descricao='Descrição do produto 1',
            preco=100.00,
            categoria=self.categoria
        )
        
        self.produto2 = Produto.objects.create(
            nome='Produto 2',
            descricao='Descrição do produto 2',
            preco=200.00,
            categoria=self.categoria
        )
        
        # Criar estoques
        self.estoque1 = Estoque.objects.create(
            produto=self.produto1,
            quantidade_atual=10,
            quantidade_reservada=0
        )
        
        self.estoque2 = Estoque.objects.create(
            produto=self.produto2,
            quantidade_atual=5,
            quantidade_reservada=0
        )
        
        # Criar pedido
        self.order = Order.objects.create(
            customer=self.customer_user,
            status='pending'
        )
        
        # Adicionar itens ao pedido
        self.order.add_item(self.produto1, 2)
        
        # Cliente API
        self.client = APIClient()
    
    def test_create_cart(self):
        """Teste de criação de carrinho."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-create-cart')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
        self.assertEqual(response.data['customer'], self.customer_user.id)
    
    def test_my_cart(self):
        """Teste de obtenção do carrinho do cliente."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-my-cart')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.order.id)
        self.assertEqual(len(response.data['items']), 1)
    
    def test_add_item(self):
        """Teste de adição de item ao pedido."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-add-item', args=[self.order.id])
        data = {
            'product_id': self.produto2.id,
            'quantity': 1
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        self.assertEqual(response.data['subtotal'], '300.00')
    
    def test_remove_item(self):
        """Teste de remoção de item do pedido."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-remove-item', args=[self.order.id])
        data = {
            'product_id': self.produto1.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)
        self.assertEqual(response.data['subtotal'], '0.00')
    
    def test_update_quantity(self):
        """Teste de atualização de quantidade de item."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-update-quantity', args=[self.order.id])
        data = {
            'product_id': self.produto1.id,
            'quantity': 3
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'][0]['quantity'], 3)
        self.assertEqual(response.data['subtotal'], '300.00')
    
    def test_finalize_order(self):
        """Teste de finalização de pedido."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-finalize', args=[self.order.id])
        data = {
            'shipping_address': 'Rua Teste, 123',
            'shipping_city': 'Cidade Teste',
            'shipping_state': 'ST',
            'shipping_zip': '12345-678',
            'notes': 'Observação de teste'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'processing')
        self.assertEqual(response.data['shipping_address'], 'Rua Teste, 123')
    
    def test_mark_as_paid(self):
        """Teste de registro de pagamento."""
        # Finalizar pedido primeiro
        self.order.shipping_address = 'Rua Teste, 123'
        self.order.shipping_city = 'Cidade Teste'
        self.order.shipping_state = 'ST'
        self.order.shipping_zip = '12345-678'
        self.order.finalize_order()
        
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('orders:pedidos-mark-as-paid', args=[self.order.id])
        data = {
            'payment_method': 'pix'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')
        self.assertEqual(response.data['payment_method'], 'pix')
    
    def test_cancel_order(self):
        """Teste de cancelamento de pedido."""
        # Finalizar pedido
        self.order.shipping_address = 'Rua Teste, 123'
        self.order.shipping_city = 'Cidade Teste'
        self.order.shipping_state = 'ST'
        self.order.shipping_zip = '12345-678'
        self.order.finalize_order()
        
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-cancel', args=[self.order.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'canceled')
    
    def test_permissions(self):
        """Teste de permissões de acesso aos pedidos."""
        # Cliente não pode ver pedidos de outros clientes
        self.client.force_authenticate(user=self.another_customer)
        url = reverse('orders:pedidos-detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # Admin pode ver qualquer pedido
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vendedor pode ver qualquer pedido
        self.client.force_authenticate(user=self.seller_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Cliente pode ver seu próprio pedido
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_my_orders(self):
        """Teste de listagem dos pedidos do cliente."""
        # Criar mais um pedido finalizado
        order2 = Order.objects.create(
            customer=self.customer_user,
            status='pending',
            shipping_address='Rua Teste, 123',
            shipping_city='Cidade Teste',
            shipping_state='ST',
            shipping_zip='12345-678'
        )
        order2.add_item(self.produto1, 1)
        order2.finalize_order()
        
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('orders:pedidos-my-orders')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas o pedido finalizado, não o carrinho
    def test_create_order_with_insufficient_stock(self):
        """Teste de criação de pedido com estoque insuficiente."""
        self.estoque1.quantidade_atual = 1
        self.estoque1.save()
        
        response = self.client.post(reverse('orders:pedidos-add-item', args=[self.order.id]), {
            'product_id': self.produto1.id,
            'quantity': 2
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Estoque insuficiente', response.data['detail'])

    def test_cancel_order_with_stock_return(self):
        """Teste de cancelamento de pedido com devolução ao estoque."""
        self.order.add_item(self.produto1, 2)
        self.order.finalize_order()
        self.order.mark_as_paid('pix')
        
        response = self.client.post(reverse('orders:pedidos-cancel', args=[self.order.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'canceled')
        
        # Verificar se o estoque foi devolvido
        estoque = Estoque.objects.get(produto=self.produto1)
        self.assertEqual(estoque.quantidade_atual, 10)
