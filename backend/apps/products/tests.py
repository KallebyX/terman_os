from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Categoria, Produto, Fornecedor
from apps.accounts.models import User


class ProductsAPITests(TestCase):
    """
    Testes para as APIs de produtos.
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
        
        self.customer_user = User.objects.create_user(
            email='customer@example.com',
            password='CustomerPassword123',
            first_name='Customer',
            last_name='User',
            user_type='customer'
        )
        
        # Criar categorias para testes
        self.categoria1 = Categoria.objects.create(
            nome='Mangueiras Hidráulicas',
            descricao='Mangueiras para sistemas hidráulicos',
            slug='mangueiras-hidraulicas',
            ativa=True,
            ordem=1
        )
        
        self.categoria2 = Categoria.objects.create(
            nome='Conexões',
            descricao='Conexões para mangueiras',
            slug='conexoes',
            ativa=True,
            ordem=2
        )
        
        # Criar produtos para testes
        self.produto1 = Produto.objects.create(
            codigo='MH001',
            nome='Mangueira Hidráulica 1/2"',
            descricao='Mangueira hidráulica de alta pressão',
            descricao_curta='Mangueira 1/2"',
            preco=100.00,
            unidade='m',
            slug='mangueira-hidraulica-1-2',
            ativo=True,
            destaque=True,
            estoque_minimo=10.00
        )
        self.produto1.categorias.add(self.categoria1)
        
        self.produto2 = Produto.objects.create(
            codigo='CN001',
            nome='Conexão Reta 1/2"',
            descricao='Conexão reta para mangueiras',
            descricao_curta='Conexão reta',
            preco=50.00,
            unidade='un',
            slug='conexao-reta-1-2',
            ativo=True,
            destaque=False,
            estoque_minimo=20.00
        )
        self.produto2.categorias.add(self.categoria2)
        
        # Criar fornecedor para testes
        self.fornecedor = Fornecedor.objects.create(
            nome='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            telefone='(11) 1234-5678',
            email='contato@fornecedor.com',
            ativo=True
        )

    def test_listar_categorias(self):
        """Teste de listagem de categorias."""
        url = reverse('products:categorias-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_detalhar_categoria(self):
        """Teste de detalhamento de categoria."""
        url = reverse('products:categorias-detail', kwargs={'slug': self.categoria1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.categoria1.nome)

    def test_criar_categoria_sem_autenticacao(self):
        """Teste de criação de categoria sem autenticação."""
        url = reverse('products:categorias-list')
        data = {
            'nome': 'Nova Categoria',
            'descricao': 'Descrição da nova categoria',
            'slug': 'nova-categoria',
            'ativa': True,
            'ordem': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_criar_categoria_com_admin(self):
        """Teste de criação de categoria com admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:categorias-list')
        data = {
            'nome': 'Nova Categoria',
            'descricao': 'Descrição da nova categoria',
            'slug': 'nova-categoria',
            'ativa': True,
            'ordem': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 3)

    def test_criar_categoria_com_cliente(self):
        """Teste de criação de categoria com cliente (não deve permitir)."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('products:categorias-list')
        data = {
            'nome': 'Nova Categoria',
            'descricao': 'Descrição da nova categoria',
            'slug': 'nova-categoria',
            'ativa': True,
            'ordem': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_produtos(self):
        """Teste de listagem de produtos."""
        url = reverse('products:produtos-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_detalhar_produto(self):
        """Teste de detalhamento de produto."""
        url = reverse('products:produtos-detail', kwargs={'pk': self.produto1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.produto1.nome)

    def test_detalhar_produto_por_slug(self):
        """Teste de detalhamento de produto por slug."""
        url = reverse('products:produto-detail-by-slug', kwargs={'slug': self.produto1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], self.produto1.nome)

    def test_criar_produto_sem_autenticacao(self):
        """Teste de criação de produto sem autenticação."""
        url = reverse('products:produtos-list')
        data = {
            'codigo': 'NOVO001',
            'nome': 'Novo Produto',
            'descricao': 'Descrição do novo produto',
            'descricao_curta': 'Novo produto',
            'preco': 75.00,
            'unidade': 'un',
            'slug': 'novo-produto',
            'ativo': True,
            'destaque': False,
            'estoque_minimo': 5.00,
            'categorias': [self.categoria1.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_criar_produto_com_admin(self):
        """Teste de criação de produto com admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:produtos-list')
        data = {
            'codigo': 'NOVO001',
            'nome': 'Novo Produto',
            'descricao': 'Descrição do novo produto',
            'descricao_curta': 'Novo produto',
            'preco': 75.00,
            'unidade': 'un',
            'slug': 'novo-produto',
            'ativo': True,
            'destaque': False,
            'estoque_minimo': 5.00,
            'categorias': [self.categoria1.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 3)

    def test_listar_produtos_destaque(self):
        """Teste de listagem de produtos em destaque."""
        url = reverse('products:produtos-destaque')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['codigo'], self.produto1.codigo)

    def test_listar_produtos_por_categoria(self):
        """Teste de listagem de produtos por categoria."""
        url = reverse('products:produtos-por-categoria', kwargs={'slug': self.categoria1.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['codigo'], self.produto1.codigo)

    def test_listar_fornecedores_sem_autenticacao(self):
        """Teste de listagem de fornecedores sem autenticação."""
        url = reverse('products:fornecedores-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_fornecedores_com_cliente(self):
        """Teste de listagem de fornecedores com cliente (não deve permitir)."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('products:fornecedores-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listar_fornecedores_com_admin(self):
        """Teste de listagem de fornecedores com admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('products:fornecedores-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['nome'], self.fornecedor.nome)
