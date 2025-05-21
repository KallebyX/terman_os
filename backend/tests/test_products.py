import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.products.models import Produto, Categoria, Fornecedor

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_categoria():
    def _create_categoria(nome='Categoria Teste', slug='categoria-teste'):
        # Verificar se já existe uma categoria com este slug para evitar erros de unicidade
        categoria, created = Categoria.objects.get_or_create(
            slug=slug,
            defaults={
                'nome': nome,
                'descricao': 'Descrição da categoria de teste',
                'ativa': True,
                'ordem': 0
            }
        )
        return categoria
    return _create_categoria

@pytest.fixture
def create_produto(create_categoria):
    def _create_produto(codigo='PROD001', nome='Produto Teste', preco=100.00):
        categoria = create_categoria()
        # Verificar se já existe um produto com este código para evitar erros de unicidade
        produto, created = Produto.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nome': nome,
                'descricao': 'Descrição do produto de teste',
                'descricao_curta': 'Produto para testes',
                'preco': preco,
                'unidade': 'un',
                'slug': f'{codigo.lower()}-{nome.lower().replace(" ", "-")}',
                'ativo': True
            }
        )
        if created:
            produto.categorias.add(categoria)
        return produto
    return _create_produto

@pytest.fixture
def create_fornecedor():
    def _create_fornecedor(nome='Fornecedor Teste'):
        fornecedor, created = Fornecedor.objects.get_or_create(
            nome=nome,
            defaults={
                'razao_social': 'Fornecedor Teste LTDA',
                'cnpj': '12.345.678/0001-90',
                'telefone': '(11) 1234-5678',
                'email': 'contato@fornecedor.com',
                'ativo': True
            }
        )
        return fornecedor
    return _create_fornecedor

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
class TestProdutosAPI:
    def test_listar_produtos(self, api_client, create_produto, admin_user):
        """Teste de listagem de produtos."""
        # Criar alguns produtos para o teste
        create_produto(codigo='PROD001', nome='Produto 1')
        create_produto(codigo='PROD002', nome='Produto 2')
        create_produto(codigo='PROD003', nome='Produto 3')
        
        # Autenticar como admin
        api_client.force_authenticate(user=admin_user)
        
        # Fazer requisição para listar produtos
        url = '/api/products/produtos/'  # URL direta em vez de reverse
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3  # Verificar se há pelo menos 3 produtos
