from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count, F, Q

from .models import Cliente, Venda, ItemVenda, FormaPagamento, Pagamento, StatusVenda, MetodoPagamentoPOS
from .serializers import (
    ClienteSerializer, VendaListSerializer, VendaDetailSerializer, 
    VendaCreateSerializer, ItemVendaSerializer, ItemVendaCreateSerializer,
    FormaPagamentoSerializer, PagamentoSerializer, VendaFinalizarSerializer,
    VendaCancelarSerializer
)
from apps.accounts.permissions import IsSellerOrAdmin
from apps.inventory.models import MovimentacaoEstoque, Estoque


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de clientes.
    Apenas administradores e vendedores podem acessar.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'ativo']
    search_fields = ['nome', 'razao_social', 'cpf', 'cnpj', 'email', 'telefone', 'celular']
    ordering_fields = ['nome', 'created_at']


class FormaPagamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de formas de pagamento.
    Apenas administradores podem criar, editar e excluir.
    Vendedores podem visualizar.
    """
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ativo', 'tipo']
    ordering_fields = ['nome']


class VendaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de vendas.
    Apenas administradores e vendedores podem acessar.
    """
    queryset = Venda.objects.all()
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'tipo', 'cliente', 'vendedor', 'nfe_emitida']
    search_fields = ['cliente__nome', 'cliente__cpf', 'cliente__cnpj', 'observacoes']
    ordering_fields = ['data_venda', 'total']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VendaListSerializer
        elif self.action == 'create':
            return VendaCreateSerializer
        return VendaDetailSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            status='aberta',
            subtotal=0,
            desconto=0,
            acréscimo=0,
            total=0
        )


class ItemVendaListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar itens de venda.
    """
    serializer_class = ItemVendaSerializer
    permission_classes = [IsSellerOrAdmin]
    
    def get_queryset(self):
        venda_id = self.kwargs['venda_id']
        return ItemVenda.objects.filter(venda_id=venda_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ItemVendaCreateSerializer
        return ItemVendaSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        venda_id = self.kwargs['venda_id']
        venda = get_object_or_404(Venda, id=venda_id)
        
        # Verificar se a venda está aberta
        if venda.status != 'aberta':
            return Response(
                {'detail': 'Não é possível adicionar itens a uma venda que não está aberta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Adicionar venda ao contexto do serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        
        # Verificar estoque
        estoque, created = Estoque.objects.get_or_create(
            produto=produto,
            defaults={'quantidade_atual': 0, 'quantidade_reservada': 0}
        )
        
        if estoque.quantidade_disponivel < quantidade:
            return Response(
                {'detail': 'Quantidade insuficiente em estoque.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reservar estoque
        estoque.quantidade_reservada += quantidade
        estoque.quantidade_atual -= quantidade
        estoque.save()
        
        # Criar item de venda e atualizar estoque
        item = ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=serializer.validated_data['preco_unitario'],
            desconto=serializer.validated_data.get('desconto', 0)
        )

        # Atualizar estoque do produto
        produto.estoque_minimo -= quantidade
        produto.save()
        
        # Atualizar totais da venda
        venda.subtotal = sum(item.subtotal for item in venda.itens.all())
        venda.total = venda.subtotal - venda.desconto + venda.acréscimo
        venda.save()
        
        return Response(
            ItemVendaSerializer(item).data,
            status=status.HTTP_201_CREATED
        )


class ItemVendaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para detalhar, atualizar e excluir itens de venda.
    """
    serializer_class = ItemVendaSerializer
    permission_classes = [IsSellerOrAdmin]
    
    def get_queryset(self):
        venda_id = self.kwargs['venda_id']
        return ItemVenda.objects.filter(venda_id=venda_id)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        item = self.get_object()
        venda = item.venda
        
        # Verificar se a venda está aberta
        if venda.status != 'aberta':
            return Response(
                {'detail': 'Não é possível alterar itens de uma venda que não está aberta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Liberar estoque reservado
        estoque = Estoque.objects.get(produto=item.produto)
        estoque.quantidade_reservada -= item.quantidade
        estoque.quantidade_atual += item.quantidade
        
        # Atualizar item
        serializer = self.get_serializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # Verificar estoque para nova quantidade
        if 'quantidade' in serializer.validated_data:
            nova_quantidade = serializer.validated_data['quantidade']
            if estoque.quantidade_disponivel < nova_quantidade:
                return Response(
                    {'detail': 'Quantidade insuficiente em estoque.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reservar nova quantidade
            estoque.quantidade_reservada += nova_quantidade
        else:
            # Manter a mesma quantidade
            estoque.quantidade_reservada += item.quantidade
        
        estoque.save()
        self.perform_update(serializer)
        
        # Atualizar totais da venda
        venda.subtotal = sum(item.subtotal for item in venda.itens.all())
        venda.total = venda.subtotal - venda.desconto + venda.acréscimo
        venda.save()
        
        return Response(serializer.data)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        venda = item.venda
        
        # Verificar se a venda está aberta
        if venda.status != 'aberta':
            return Response(
                {'detail': 'Não é possível remover itens de uma venda que não está aberta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Liberar estoque reservado
        estoque = Estoque.objects.get(produto=item.produto)
        estoque.quantidade_reservada -= item.quantidade
        estoque.save()
        
        # Excluir item
        self.perform_destroy(item)
        
        # Atualizar totais da venda
        venda.subtotal = sum(i.subtotal for i in venda.itens.all())
        venda.total = venda.subtotal - venda.desconto + venda.acréscimo
        venda.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class PagamentoListView(generics.ListAPIView):
    """
    View para listar pagamentos de uma venda.
    """
    serializer_class = PagamentoSerializer
    permission_classes = [IsSellerOrAdmin]
    
    def get_queryset(self):
        venda_id = self.kwargs['venda_id']
        return Pagamento.objects.filter(venda_id=venda_id)


class VendaFinalizarView(APIView):
    """
    View para finalizar uma venda.
    """
    permission_classes = [IsSellerOrAdmin]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Venda, id=pk)

    def post(self, request, *args, **kwargs):
        """
        Processa uma venda.

        Processa a venda com base nos itens e forma de pagamento informados.
        Caso a venda seja processada com sucesso, retorna um objeto com chave 'status'
        e valor 'Venda processada com sucesso'. Caso contrário, retorna um objeto com
        chave 'error' e valor com a descrição do erro.

        :param request: Requisição HTTP.
        :type request: rest_framework.request.Request
        :param args: Argumentos adicionais.
        :type args: list
        :param kwargs: Dicionário de argumentos nomeados.
        :type kwargs: dict
        :return: Resposta HTTP com o status da venda.
        :rtype: rest_framework.response.Response
        """
        venda = self.get_object()
        
        # Verificar se a venda já está finalizada
        if venda.status != 'aberta':
            return Response(
                {"error": "Esta venda não está aberta para finalização."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se a venda tem itens
        if not venda.itens.exists():
            return Response(
                {"error": "Não é possível finalizar uma venda sem itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se o pagamento foi informado
        if 'pagamentos' not in request.data or not request.data['pagamentos']:
            return Response(
                {"error": "É necessário informar pelo menos um pagamento."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Processar pagamentos
            pagamentos_data = request.data['pagamentos']
            total_pagamentos = 0
            
            # Validar pagamentos
            for pagamento_data in pagamentos_data:
                if 'forma_pagamento' not in pagamento_data:
                    return Response(
                        {"error": "Forma de pagamento não informada."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if 'valor' not in pagamento_data:
                    return Response(
                        {"error": "Valor do pagamento não informado."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                total_pagamentos += float(pagamento_data['valor'])
            
            # Verificar se o total de pagamentos cobre o valor da venda
            if total_pagamentos < float(venda.total):
                return Response(
                    {"error": f"O valor total dos pagamentos ({total_pagamentos}) é menor que o valor da venda ({venda.total})."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Processar a venda
            venda.processar_venda()
            
            # Registrar pagamentos
            for pagamento_data in pagamentos_data:
                forma_pagamento = get_object_or_404(
                    FormaPagamento, 
                    id=pagamento_data['forma_pagamento']
                )
                
                Pagamento.objects.create(
                    venda=venda,
                    forma_pagamento=forma_pagamento,
                    valor=pagamento_data['valor'],
                    status='aprovado',
                    parcelas=pagamento_data.get('parcelas', 1),
                    autorizacao=pagamento_data.get('autorizacao'),
                    bandeira=pagamento_data.get('bandeira'),
                    nsu=pagamento_data.get('nsu')
                )
            
            return Response({
                "status": "Venda processada com sucesso",
                "venda_id": venda.id,
                "total": venda.total,
                "data_finalizacao": venda.data_finalizacao
            })
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Erro inesperado ao processar a venda: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VendaCancelarView(APIView):
    """
    View para cancelar uma venda.
    """
    permission_classes = [IsSellerOrAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        venda = get_object_or_404(Venda, id=pk)
        
        # Verificar se a venda pode ser cancelada
        if venda.status == 'cancelada':
            return Response(
                {'detail': 'Esta venda já está cancelada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = VendaCancelarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Se a venda estava finalizada, devolver ao estoque
        if venda.status == 'finalizada':
            for item in venda.itens.all():
                estoque, created = Estoque.objects.get_or_create(
                    produto=item.produto,
                    defaults={'quantidade_atual': 0, 'quantidade_reservada': 0}
                )
                estoque.quantidade_atual += item.quantidade
                estoque.save()
                
                # Registrar movimentação
                MovimentacaoEstoque.objects.create(
                    produto=item.produto,
                    tipo='entrada',
                    origem='devolucao',
                    quantidade=item.quantidade,
                    valor_unitario=item.preco_unitario,
                    documento=f"Cancelamento Venda #{venda.id}",
                    observacao=serializer.validated_data['motivo'],
                    usuario=request.user,
                    referencia_id=venda.id,
                    referencia_tipo='venda_cancelada'
                )
        else:  # Se estava aberta, liberar reservas
            for item in venda.itens.all():
                estoque = Estoque.objects.get(produto=item.produto)
                estoque.quantidade_reservada -= item.quantidade
                estoque.save()
        
        # Cancelar venda
        venda.status = 'cancelada'
        venda.data_cancelamento = timezone.now()
        venda.motivo_cancelamento = serializer.validated_data['motivo']
        venda.save()
        
        return Response(
            VendaDetailSerializer(venda).data,
            status=status.HTTP_200_OK
        )


class RelatorioVendasView(APIView):
    """
    View para gerar relatório de vendas.
    """
    permission_classes = [IsSellerOrAdmin]
    
    def get(self, request):
        # Parâmetros de filtro
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        status = request.query_params.get('status')
        tipo = request.query_params.get('tipo')
        cliente_id = request.query_params.get('cliente_id')
        vendedor_id = request.query_params.get('vendedor_id')
        
        # Base da query
        queryset = Venda.objects.all()
        
        # Aplicar filtros
        if data_inicio:
            queryset = queryset.filter(data_venda__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_venda__lte=data_fim)
        if status:
            queryset = queryset.filter(status=status)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if vendedor_id:
            queryset = queryset.filter(vendedor_id=vendedor_id)
        
        # Calcular totais
        total_vendas = queryset.count()
        total_valor = sum(venda.total for venda in queryset)
        
        # Agrupar por forma de pagamento
        pagamentos = Pagamento.objects.filter(venda__in=queryset)
        pagamentos_por_forma = {}
        for pagamento in pagamentos:
            forma = pagamento.forma_pagamento.nome
            if forma not in pagamentos_por_forma:
                pagamentos_por_forma[forma] = 0
            pagamentos_por_forma[forma] += pagamento.valor
        
        return Response({
            'total_vendas': total_vendas,
            'total_valor': total_valor,
            'pagamentos_por_forma': pagamentos_por_forma,
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim or timezone.now().date().isoformat()
            }
        })


class DashboardVendasView(APIView):
    """
    View para dashboard de vendas.
    """
    permission_classes = [IsSellerOrAdmin]
    
    def get(self, request):
        # Vendas do dia
        hoje = timezone.now().date()
        vendas_hoje = Venda.objects.filter(
            data_venda__date=hoje,
            status='finalizada'
        )
        
        # Vendas da semana
        inicio_semana = hoje - timezone.timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timezone.timedelta(days=6)
        vendas_semana = Venda.objects.filter(
            data_venda__date__range=[inicio_semana, fim_semana],
            status='finalizada'
        )
        
        # Vendas do mês
        inicio_mes = hoje.replace(day=1)
        if hoje.month == 12:
            fim_mes = hoje.replace(year=hoje.year + 1, month=1, day=1) - timezone.timedelta(days=1)
        else:
            fim_mes = hoje.replace(month=hoje.month + 1, day=1) - timezone.timedelta(days=1)
        vendas_mes = Venda.objects.filter(
            data_venda__date__range=[inicio_mes, fim_mes],
            status='finalizada'
        )
        
        # Top produtos
        from django.db.models import Sum
        top_produtos = ItemVenda.objects.filter(
            venda__status='finalizada',
            venda__data_venda__date__range=[inicio_mes, fim_mes]
        ).values(
            'produto__nome', 'produto__codigo'
        ).annotate(
            total_quantidade=Sum('quantidade'),
            total_valor=Sum('subtotal')
        ).order_by('-total_valor')[:5]
        
        return Response({
            'vendas_hoje': {
                'quantidade': vendas_hoje.count(),
                'valor': sum(v.total for v in vendas_hoje)
            },
            'vendas_semana': {
                'quantidade': vendas_semana.count(),
                'valor': sum(v.total for v in vendas_semana)
            },
            'vendas_mes': {
                'quantidade': vendas_mes.count(),
                'valor': sum(v.total for v in vendas_mes)
            },
            'top_produtos': top_produtos,
            'periodo': {
                'hoje': hoje.isoformat(),
                'inicio_semana': inicio_semana.isoformat(),
                'fim_semana': fim_semana.isoformat(),
                'inicio_mes': inicio_mes.isoformat(),
                'fim_mes': fim_mes.isoformat()
            }
        })
