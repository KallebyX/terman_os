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
    # Verificar se o usuário já existe para evitar erros de duplicação
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
class TestProdutosAPI:
    def test_listar_produtos(self, api_client, create_produto, admin_user, get_jwt_token):
        """Teste de listagem de produtos."""
        # Criar alguns produtos para o teste
        create_produto(codigo='PROD001', nome='Produto 1')
        create_produto(codigo='PROD002', nome='Produto 2')
        create_produto(codigo='PROD003', nome='Produto 3')
        
        # Autenticar usando JWT
        token = get_jwt_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Fazer requisição para listar produtos
        url = '/api/products/produtos/'  # URL direta em vez de reverse
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3  # Verificar se há pelo menos 3 produtos
        
    def test_detalhe_produto(self, api_client, create_produto, admin_user, get_jwt_token):
        """Teste de detalhe de produto."""
        produto = create_produto(codigo='PROD004', nome='Produto Detalhe', preco=150.00)
        
        # Autenticar usando JWT
        token = get_jwt_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Fazer requisição para detalhe do produto
        url = f'/api/products/produtos/{produto.id}/'
        response = api_client.get(url)
        
        # Verificar resposta
        assert response.status_code == status.HTTP_200_OK
        assert response.data['codigo'] == 'PROD004'
        assert response.data['nome'] == 'Produto Detalhe'
        assert float(response.data['preco']) == 150.00
        
    def test_criar_produto(self, api_client, create_categoria, admin_user, get_jwt_token):
        """Teste de criação de produto."""
        categoria = create_categoria(nome='Categoria Nova', slug='categoria-nova')
        
        # Autenticar usando JWT
        token = get_jwt_token(admin_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Dados para o novo produto
        data = {
            'codigo': 'PROD005',
            'nome': 'Produto Novo',
            'descricao': 'Descrição do produto novo',
            'descricao_curta': 'Produto novo para testes',
            'preco': 200.00,
            'unidade': 'un',
            'slug': 'prod005-produto-novo',
            'ativo': True,
            'categorias': [categoria.id]
        }
        
        # Fazer requisição para criar produto
        url = '/api/products/produtos/'
        response = api_client.post(url, data, format='json')
        
        # Verificar resposta
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['codigo'] == 'PROD005'
        assert response.data['nome'] == 'Produto Novo'
        assert float(response.data['preco']) == 200.00
        
        # Verificar se o produto foi realmente criado no banco
        produto = Produto.objects.get(codigo='PROD005')
        assert produto.nome == 'Produto Novo'
