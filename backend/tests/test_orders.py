import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.orders.models import Order, OrderItem
from apps.products.models import Produto
from apps.accounts.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_produto():
    def _create_produto(codigo='PROD001', nome='Produto Teste', preco=100.00):
        produto, created = Produto.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nome': nome,
                'descricao': 'Descrição do produto de teste',
                'descricao_curta': 'Produto para testes',
                'preco': preco,
                'unidade': 'un',
                'slug': f'{codigo.lower()}-{nome.lower().replace(" ", "-")}',
                'ativo': True,
                'estoque_minimo': 10
            }
        )
        return produto
    return _create_produto

@pytest.fixture
def create_cliente(django_user_model):
    def _create_cliente(email=None, password='ClientePassword123'):
        # Gerar email único para evitar erros de integridade
        if email is None:
            import uuid
            email = f'cliente_{uuid.uuid4().hex[:8]}@example.com'
            
        cliente = django_user_model.objects.create_user(
            email=email,
            password=password,
            first_name='Cliente',
            last_name='Teste',
            is_admin=False
        )
        return cliente
    return _create_cliente

@pytest.fixture
def create_order(create_cliente, create_produto):
    def _create_order(customer=None, produtos=None, status_order='pending'):
        if customer is None:
            customer = create_cliente()
        
        order = Order.objects.create(
            customer=customer,
            status=status_order,
            total=0,
            notes='Pedido de teste'
        )
        
        total = 0
        if produtos:
            for produto_info in produtos:
                produto = produto_info.get('produto', create_produto())
                quantity = produto_info.get('quantidade', 1)
                
                OrderItem.objects.create(
                    order=order,
                    product=produto,
                    quantity=quantity,
                    price=produto.preco
                )
                
                total += produto.preco * quantity
        
        order.total = total
        order.save()
        
        return order
    return _create_order

@pytest.fixture
def admin_user(django_user_model):
    # Usar try/except para evitar erros de duplicação
    try:
        admin = django_user_model.objects.get(email='admin@example.com')
    except django_user_model.DoesNotExist:
        admin = django_user_model.objects.create_superuser(
            email='admin@example.com',
            password='AdminPassword123',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
    return admin

@pytest.mark.django_db
class TestOrdersAPI:
    def test_listar_orders(self, api_client, create_order, create_produto, admin_user):
        """Teste de listagem de pedidos."""
        # Criar alguns pedidos para o teste
        produto1 = create_produto(codigo='PROD001', nome='Produto 1', preco=100.00)
        produto2 = create_produto(codigo='PROD002', nome='Produto 2', preco=200.00)
        
        create_order(produtos=[{'produto': produto1, 'quantidade': 2}])
        create_order(produtos=[{'produto': produto2, 'quantidade': 1}])
        create_order(produtos=[
            {'produto': produto1, 'quantidade': 1},
            {'produto': produto2, 'quantidade': 1}
        ])
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Fazer requisição para listar pedidos
        url = '/api/orders/orders/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        # Verificar se há pelo menos 3 pedidos no campo 'results' da resposta paginada
        assert len(response.data['results']) >= 3
    
    def test_detalhe_order(self, api_client, create_order, create_produto, admin_user):
        """Teste de detalhe de pedido."""
        # Criar pedido para o teste
        produto1 = create_produto(codigo='PROD003', nome='Produto Detalhe', preco=150.00)
        produto2 = create_produto(codigo='PROD004', nome='Produto Detalhe 2', preco=250.00)
        
        order = create_order(produtos=[
            {'produto': produto1, 'quantidade': 2},
            {'produto': produto2, 'quantidade': 1}
        ])
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Fazer requisição para detalhe do pedido
        url = f'/api/orders/orders/{order.id}/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == order.id
        assert float(response.data['total']) == 550.00  # (150*2) + (250*1)
        assert len(response.data['items']) == 2  # Verificar se há 2 itens no pedido
    
    def test_cliente_ve_apenas_seus_orders(self, api_client, create_order, create_cliente, create_produto):
        """Teste de que cliente só vê seus próprios pedidos."""
        # Criar clientes e produtos
        cliente1 = create_cliente(email='cliente1_unique@example.com')
        cliente2 = create_cliente(email='cliente2_unique@example.com')
        produto = create_produto(codigo='PROD005', nome='Produto Cliente', preco=100.00)
        
        # Criar pedidos para diferentes clientes
        order_cliente1 = create_order(customer=cliente1, produtos=[{'produto': produto, 'quantidade': 1}])
        order_cliente2 = create_order(customer=cliente2, produtos=[{'produto': produto, 'quantidade': 2}])
        
        # Autenticar como cliente1
        api_client.force_authenticate(user=cliente1)
        
        # Fazer requisição para listar pedidos
        url = '/api/orders/my-orders/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        # Ajustado para acessar o campo 'results' da resposta paginada
        assert len(response.data['results']) == 1  # Cliente1 deve ver apenas 1 pedido
        assert response.data['results'][0]['id'] == order_cliente1.id
        
        # Cliente1 não deve conseguir ver pedido do cliente2
        url = f'/api/orders/orders/{order_cliente2.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_atualizar_status_order(self, api_client, create_order, create_produto, admin_user):
        """Teste de atualização de status de pedido."""
        # Criar pedido para o teste
        produto = create_produto(codigo='PROD006', nome='Produto Status', preco=100.00)
        order = create_order(produtos=[{'produto': produto, 'quantidade': 1}], status_order='pending')
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Dados para atualização do status
        data = {
            'status': 'processing'
        }
        
        # Fazer requisição para atualizar status
        url = f'/api/orders/orders/{order.id}/'
        response = api_client.patch(url, data, format='json')
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'processing'
        
        # Verificar se o pedido foi realmente atualizado no banco
        order.refresh_from_db()
        assert order.status == 'processing'
