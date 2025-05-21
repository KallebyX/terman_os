from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Cliente, Venda, ItemVenda, FormaPagamento, Pagamento
from apps.products.models import Produto, Categoria
from apps.accounts.models import User
from apps.inventory.models import Estoque, MovimentacaoEstoque
from django.utils import timezone


class PosAPITests(TestCase):
    """
    Testes para as APIs do módulo PDV.
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
        
        # Criar clientes para testes
        self.cliente_pf = Cliente.objects.create(
            tipo='pf',
            nome='João Silva',
            email='joao@example.com',
            telefone='(11) 98765-4321',
            cpf='123.456.789-00',
            endereco='Rua Exemplo',
            cidade='São Paulo',
            estado='SP',
            ativo=True
        )
        
        self.cliente_pj = Cliente.objects.create(
            tipo='pj',
            nome='Empresa XYZ',
            razao_social='Empresa XYZ Ltda',
            email='contato@xyz.com',
            telefone='(11) 1234-5678',
            cnpj='12.345.678/0001-90',
            endereco='Av Comercial',
            cidade='São Paulo',
            estado='SP',
            ativo=True
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
            quantidade_reservada=0.00
        )
        
        self.estoque2 = Estoque.objects.create(
            produto=self.produto2,
            quantidade_atual=10.00,
            quantidade_reservada=0.00
        )
        
        # Criar formas de pagamento para testes
        self.forma_pagamento1 = FormaPagamento.objects.create(
            nome='Dinheiro',
            tipo='dinheiro',
            ativo=True
        )
        
        self.forma_pagamento2 = FormaPagamento.objects.create(
            nome='Cartão de Crédito',
            tipo='cartao_credito',
            ativo=True,
            taxa=2.5
        )
        
        # Criar venda para testes
        self.venda = Venda.objects.create(
            cliente=self.cliente_pf,
            vendedor=self.seller_user,
            status='aberta',
            tipo='balcao'
        )

    def test_listar_clientes_com_admin(self):
        """Teste de listagem de clientes com admin."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('pos:clientes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_listar_clientes_com_vendedor(self):
        """Teste de listagem de clientes com vendedor."""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('pos:clientes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_listar_clientes_com_cliente(self):
        """Teste de listagem de clientes com cliente (não deve permitir)."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('pos:clientes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_criar_cliente(self):
        """Teste de criação de cliente."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('pos:clientes-list')
        data = {
            'tipo': 'pf',
            'nome': 'Maria Souza',
            'email': 'maria@example.com',
            'telefone': '(11) 91234-5678',
            'cpf': '987.654.321-00',
            'endereco': 'Rua Nova',
            'cidade': 'Rio de Janeiro',
            'estado': 'RJ',
            'ativo': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 3)
        self.assertEqual(Cliente.objects.get(cpf='987.654.321-00').nome, 'Maria Souza')

    def test_criar_venda(self):
        """Teste de criação de venda."""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('pos:vendas-list')
        data = {
            'cliente': self.cliente_pf.id,
            'vendedor': self.seller_user.id,
            'tipo': 'balcao',
            'observacoes': 'Venda de teste'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venda.objects.count(), 2)
        self.assertEqual(response.data['status'], 'aberta')

    def test_adicionar_item_venda(self):
        """Teste de adição de item à venda."""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('pos:venda-itens', kwargs={'venda_id': self.venda.id})
        data = {
            'produto': self.produto1.id,
            'quantidade': 5.00,
            'preco_unitario': 100.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemVenda.objects.count(), 1)
        
        # Verificar se o estoque foi reservado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_reservada), 5.00)
        
        # Verificar se os totais da venda foram atualizados
        self.venda.refresh_from_db()
        self.assertEqual(float(self.venda.subtotal), 500.00)
        self.assertEqual(float(self.venda.total), 500.00)

    def test_finalizar_venda(self):
        """Teste de finalização de venda."""
        self.client.force_authenticate(user=self.seller_user)
        
        # Adicionar item à venda
        item = ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto1,
            quantidade=5.00,
            preco_unitario=100.00,
            subtotal=500.00
        )
        
        # Reservar estoque
        self.estoque1.quantidade_reservada = 5.00
        self.estoque1.save()
        
        # Atualizar totais da venda
        self.venda.subtotal = 500.00
        self.venda.total = 500.00
        self.venda.save()
        
        # Finalizar venda
        url = reverse('pos:venda-finalizar', kwargs={'pk': self.venda.id})
        data = {
            'pagamentos': [
                {
                    'forma_pagamento': self.forma_pagamento1.id,
                    'valor': 500.00
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a venda foi finalizada
        self.venda.refresh_from_db()
        self.assertEqual(self.venda.status, 'finalizada')
        self.assertIsNotNone(self.venda.data_finalizacao)
        
        # Verificar se o pagamento foi registrado
        self.assertEqual(Pagamento.objects.count(), 1)
        pagamento = Pagamento.objects.first()
        self.assertEqual(pagamento.forma_pagamento, self.forma_pagamento1)
        self.assertEqual(float(pagamento.valor), 500.00)
        
        # Verificar se o estoque foi atualizado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_reservada), 0.00)
        self.assertEqual(float(self.estoque1.quantidade_atual), 15.00)
        
        # Verificar se a movimentação foi registrada
        self.assertEqual(MovimentacaoEstoque.objects.count(), 1)
        movimentacao = MovimentacaoEstoque.objects.first()
        self.assertEqual(movimentacao.produto, self.produto1)
        self.assertEqual(movimentacao.tipo, 'saida')
        self.assertEqual(movimentacao.origem, 'venda')
        self.assertEqual(float(movimentacao.quantidade), 5.00)

    def test_cancelar_venda(self):
        """Teste de cancelamento de venda."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Adicionar item à venda e finalizar
        item = ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto1,
            quantidade=5.00,
            preco_unitario=100.00,
            subtotal=500.00
        )
        
        # Atualizar estoque (como se a venda tivesse sido finalizada)
        self.estoque1.quantidade_atual = 15.00
        self.estoque1.save()
        
        # Atualizar venda como finalizada
        self.venda.status = 'finalizada'
        self.venda.subtotal = 500.00
        self.venda.total = 500.00
        self.venda.data_finalizacao = timezone.now()
        self.venda.save()
        
        # Registrar pagamento
        pagamento = Pagamento.objects.create(
            venda=self.venda,
            forma_pagamento=self.forma_pagamento1,
            valor=500.00,
            status='aprovado'
        )
        
        # Cancelar venda
        url = reverse('pos:venda-cancelar', kwargs={'pk': self.venda.id})
        data = {
            'motivo': 'Cliente desistiu da compra'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se a venda foi cancelada
        self.venda.refresh_from_db()
        self.assertEqual(self.venda.status, 'cancelada')
        self.assertIsNotNone(self.venda.data_cancelamento)
        self.assertEqual(self.venda.motivo_cancelamento, 'Cliente desistiu da compra')
        
        # Verificar se o estoque foi restaurado
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_atual), 20.00)
        
        # Verificar se a movimentação foi registrada
        self.assertEqual(MovimentacaoEstoque.objects.count(), 1)
        movimentacao = MovimentacaoEstoque.objects.first()
        self.assertEqual(movimentacao.produto, self.produto1)
        self.assertEqual(movimentacao.tipo, 'entrada')
        self.assertEqual(movimentacao.origem, 'devolucao')
        self.assertEqual(float(movimentacao.quantidade), 5.00)

    def test_relatorio_vendas(self):
        """Teste de relatório de vendas."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Criar algumas vendas finalizadas
        venda1 = Venda.objects.create(
            cliente=self.cliente_pf,
            vendedor=self.seller_user,
            status='finalizada',
            tipo='balcao',
            subtotal=500.00,
            total=500.00,
            data_finalizacao=timezone.now()
        )
        
        venda2 = Venda.objects.create(
            cliente=self.cliente_pj,
            vendedor=self.admin_user,
            status='finalizada',
            tipo='entrega',
            subtotal=1000.00,
            total=1000.00,
            data_finalizacao=timezone.now()
        )
        
        # Registrar pagamentos
        Pagamento.objects.create(
            venda=venda1,
            forma_pagamento=self.forma_pagamento1,
            valor=500.00,
            status='aprovado'
        )
        
        Pagamento.objects.create(
            venda=venda2,
            forma_pagamento=self.forma_pagamento2,
            valor=1000.00,
            status='aprovado'
        )
        
        # Acessar relatório
        url = reverse('pos:relatorio-vendas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar dados do relatório
        self.assertEqual(response.data['total_vendas'], 2)
        self.assertEqual(float(response.data['total_valor']), 1500.00)
        self.assertEqual(len(response.data['pagamentos_por_forma']), 2)
        self.assertEqual(float(response.data['pagamentos_por_forma']['Dinheiro']), 500.00)
        self.assertEqual(float(response.data['pagamentos_por_forma']['Cartão de Crédito']), 1000.00)

    def test_dashboard_vendas(self):
        """Teste de dashboard de vendas."""
        self.client.force_authenticate(user=self.admin_user)
        
        # Criar algumas vendas finalizadas
        hoje = timezone.now().date()
        
        venda1 = Venda.objects.create(
            cliente=self.cliente_pf,
            vendedor=self.seller_user,
            status='finalizada',
            tipo='balcao',
            subtotal=500.00,
            total=500.00,
            data_finalizacao=timezone.now()
        )
        
        venda2 = Venda.objects.create(
            cliente=self.cliente_pj,
            vendedor=self.admin_user,
            status='finalizada',
            tipo='entrega',
            subtotal=1000.00,
            total=1000.00,
            data_finalizacao=timezone.now()
        )
        
        # Acessar dashboard
        url = reverse('pos:dashboard-vendas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar dados do dashboard
        self.assertEqual(response.data['vendas_hoje']['quantidade'], 2)
        self.assertEqual(float(response.data['vendas_hoje']['valor']), 1500.00)
        self.assertEqual(response.data['vendas_semana']['quantidade'], 2)
        self.assertEqual(float(response.data['vendas_semana']['valor']), 1500.00)
        self.assertEqual(response.data['vendas_mes']['quantidade'], 2)
        self.assertEqual(float(response.data['vendas_mes']['valor']), 1500.00)
    def test_estoque_atualizacao_ao_adicionar_item(self):
        """Teste de atualização de estoque ao adicionar item à venda."""
        self.client.force_authenticate(user=self.seller_user)
        url = reverse('pos:venda-itens', kwargs={'venda_id': self.venda.id})
        data = {
            'produto': self.produto1.id,
            'quantidade': 5.00,
            'preco_unitario': 100.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar se o estoque foi atualizado corretamente
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_reservada), 5.00)
        self.assertEqual(float(self.estoque1.quantidade_atual), 15.00)

    def test_estoque_atualizacao_ao_remover_item(self):
        """Teste de atualização de estoque ao remover item da venda."""
        self.client.force_authenticate(user=self.seller_user)
        
        # Adicionar item à venda
        item = ItemVenda.objects.create(
            venda=self.venda,
            produto=self.produto1,
            quantidade=5.00,
            preco_unitario=100.00,
            subtotal=500.00
        )
        
        # Atualizar estoque
        self.estoque1.quantidade_reservada = 5.00
        self.estoque1.quantidade_atual = 15.00
        self.estoque1.save()
        
        # Remover item
        url = reverse('pos:venda-item-detail', kwargs={'venda_id': self.venda.id, 'pk': item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar se o estoque foi atualizado corretamente
        self.estoque1.refresh_from_db()
        self.assertEqual(float(self.estoque1.quantidade_reservada), 0.00)
        self.assertEqual(float(self.estoque1.quantidade_atual), 20.00)
