import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.inventory.models import Estoque, MovimentacaoEstoque
from apps.products.models import Produto

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
def create_estoque(create_produto):
    def _create_estoque(produto=None, quantidade=50):
        if produto is None:
            produto = create_produto()
        
        estoque, created = Estoque.objects.get_or_create(
            produto=produto,
            defaults={
                'quantidade_atual': quantidade,
                'quantidade_reservada': 0
            }
        )
        
        if not created:
            estoque.quantidade_atual = quantidade
            estoque.quantidade_reservada = 0
            estoque.save()
            
        return estoque
    return _create_estoque

@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        email='admin@example.com',
        password='AdminPassword123',
        first_name='Admin',
        last_name='User',
        is_admin=True
    )

@pytest.mark.django_db
class TestInventoryAPI:
    def test_listar_estoque(self, api_client, create_estoque, create_produto, admin_user):
        """Teste de listagem de estoque."""
        # Criar alguns itens de estoque para o teste
        produto1 = create_produto(codigo='PROD001', nome='Produto 1')
        produto2 = create_produto(codigo='PROD002', nome='Produto 2')
        produto3 = create_produto(codigo='PROD003', nome='Produto 3')
        
        create_estoque(produto=produto1, quantidade=100)
        create_estoque(produto=produto2, quantidade=50)
        create_estoque(produto=produto3, quantidade=25)
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Fazer requisição para listar estoque
        url = '/api/inventory/estoque/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3  # Verificar se há pelo menos 3 itens de estoque
    
    def test_detalhe_estoque(self, api_client, create_estoque, create_produto, admin_user):
        """Teste de detalhe de estoque."""
        # Criar estoque para o teste
        produto = create_produto(codigo='PROD004', nome='Produto Teste Estoque')
        estoque = create_estoque(produto=produto, quantidade=75)
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Fazer requisição para detalhe do estoque
        url = f'/api/inventory/estoque/{estoque.id}/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.data['produto']['codigo'] == 'PROD004'
        # Ajustado para comparar com string, já que a API retorna valores decimais como strings
        assert response.data['quantidade_atual'] == '75.00'
        assert float(response.data['quantidade_disponivel']) == 75.0  # Sem reservas
    
    def test_listar_movimentacoes(self, api_client, create_estoque, create_produto, admin_user):
        """Teste de listagem de movimentações de estoque."""
        # Criar estoque e movimentações para o teste
        produto = create_produto(codigo='PROD006', nome='Produto Movimentações')
        estoque = create_estoque(produto=produto, quantidade=200)
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Criar algumas movimentações
        MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='entrada',
            origem='compra',
            quantidade=50,
            valor_unitario=90.00,
            observacao='Entrada teste 1',
            usuario=admin_user
        )
        
        MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='saida',
            origem='venda',
            quantidade=20,
            valor_unitario=100.00,
            observacao='Saída teste 1',
            usuario=admin_user
        )
        
        # Fazer requisição para listar movimentações
        url = '/api/inventory/movimentacoes/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2  # Verificar se há pelo menos 2 movimentações
