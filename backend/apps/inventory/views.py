from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Estoque, MovimentacaoEstoque
from .serializers import EstoqueSerializer, MovimentacaoEstoqueSerializer, AjusteEstoqueSerializer
from apps.products.models import Produto
from apps.accounts.permissions import IsSellerOrAdmin
from rest_framework.permissions import IsAdminUser


class EstoqueViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de estoque.
    Apenas administradores e vendedores podem acessar.
    """
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializer
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['produto__ativo', 'produto__categorias']
    search_fields = ['produto__nome', 'produto__codigo']
    ordering_fields = ['produto__nome', 'quantidade_atual', 'ultima_atualizacao']


class MovimentacaoEstoqueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualização de movimentações de estoque.
    Apenas administradores e vendedores podem acessar.
    """
    queryset = MovimentacaoEstoque.objects.all()
    serializer_class = MovimentacaoEstoqueSerializer
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['produto', 'tipo', 'origem', 'data_movimentacao']
    search_fields = ['produto__nome', 'produto__codigo', 'documento', 'observacao']
    ordering_fields = ['data_movimentacao', 'produto__nome']


class AjusteEstoqueView(APIView):
    """
    View para realizar ajustes de estoque.
    Apenas administradores e vendedores podem acessar.
    """
    permission_classes = [IsSellerOrAdmin]
    
    @transaction.atomic
    def post(self, request):
        serializer = AjusteEstoqueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        produto_id = serializer.validated_data['produto_id']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']
        origem = serializer.validated_data['origem']
        documento = serializer.validated_data.get('documento', '')
        observacao = serializer.validated_data.get('observacao', '')
        valor_unitario = serializer.validated_data.get('valor_unitario')
        referencia_id = serializer.validated_data.get('referencia_id')
        referencia_tipo = serializer.validated_data.get('referencia_tipo')
        
        # Obter o produto
        produto = get_object_or_404(Produto, id=produto_id)
        
        # Obter ou criar o estoque
        estoque, created = Estoque.objects.get_or_create(
            produto=produto,
            defaults={'quantidade_atual': 0, 'quantidade_reservada': 0}
        )
        
        # Atualizar o estoque
        if tipo == 'entrada':
            estoque.quantidade_atual += quantidade
        elif tipo == 'saida':
            if estoque.quantidade_disponivel < quantidade:
                return Response(
                    {'detail': 'Quantidade insuficiente em estoque.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            estoque.quantidade_atual -= quantidade
        elif tipo == 'ajuste':
            estoque.quantidade_atual = quantidade
        
        estoque.save()
        
        # Registrar a movimentação
        movimentacao = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo=tipo,
            origem=origem,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            documento=documento,
            observacao=observacao,
            usuario=request.user,
            referencia_id=referencia_id,
            referencia_tipo=referencia_tipo
        )
        
        return Response({
            'estoque': EstoqueSerializer(estoque).data,
            'movimentacao': MovimentacaoEstoqueSerializer(movimentacao).data
        }, status=status.HTTP_201_CREATED)


class ProdutosBaixoEstoqueView(generics.ListAPIView):
    """
    View para listar produtos com estoque baixo ou esgotado.
    Apenas administradores e vendedores podem acessar.
    """
    serializer_class = EstoqueSerializer
    permission_classes = [IsSellerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['produto__nome', 'quantidade_atual']
    
    def get_queryset(self):
        queryset = Estoque.objects.all()
        
        # Filtrar por produtos com estoque baixo
        queryset = queryset.filter(
            quantidade_disponivel__lt=models.F('produto__estoque_minimo')
        )
        
        return queryset


class RelatorioMovimentacoesView(APIView):
    """
    View para gerar relatório de movimentações de estoque.
    Apenas administradores e vendedores podem acessar.
    """
    permission_classes = [IsSellerOrAdmin]
    
    def get(self, request):
        # Parâmetros de filtro
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        tipo = request.query_params.get('tipo')
        origem = request.query_params.get('origem')
        produto_id = request.query_params.get('produto_id')
        
        # Base da query
        queryset = MovimentacaoEstoque.objects.all()
        
        # Aplicar filtros
        if data_inicio:
            queryset = queryset.filter(data_movimentacao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_movimentacao__lte=data_fim)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if origem:
            queryset = queryset.filter(origem=origem)
        if produto_id:
            queryset = queryset.filter(produto_id=produto_id)
        
        # Serializar resultados
        serializer = MovimentacaoEstoqueSerializer(queryset, many=True)
        
        # Calcular totais
        total_entradas = sum(
            m.quantidade for m in queryset if m.tipo == 'entrada'
        )
        total_saidas = sum(
            m.quantidade for m in queryset if m.tipo == 'saida'
        )
        
        return Response({
            'movimentacoes': serializer.data,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'saldo': total_entradas - total_saidas,
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim or timezone.now().date().isoformat()
            }
        })
