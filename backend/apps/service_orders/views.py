from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import OrdemServico, ItemOrdemServico, EtapaOrdemServico, ComentarioOrdemServico, AnexoOrdemServico
from .serializers import (
    OrdemServicoListSerializer, OrdemServicoDetailSerializer, OrdemServicoCreateSerializer,
    OrdemServicoUpdateSerializer, OrdemServicoStatusUpdateSerializer, OrdemServicoCancelarSerializer,
    ItemOrdemServicoSerializer, EtapaOrdemServicoSerializer, ComentarioOrdemServicoSerializer,
    AnexoOrdemServicoSerializer
)
from apps.accounts.permissions import IsOperatorOrAdmin, IsSellerOrAdmin
from apps.inventory.models import MovimentacaoEstoque, Estoque


class OrdemServicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de ordens de serviço.
    Apenas administradores, vendedores e operadores podem acessar.
    """
    permission_classes = [IsOperatorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'prioridade', 'cliente', 'responsavel', 'tecnico']
    search_fields = ['numero', 'cliente__nome', 'descricao_problema', 'descricao_servico']
    ordering_fields = ['data_abertura', 'prioridade', 'status']
    
    def get_queryset(self):
        return OrdemServico.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrdemServicoListSerializer
        elif self.action == 'create':
            return OrdemServicoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrdemServicoUpdateSerializer
        return OrdemServicoDetailSerializer


class EtapaOrdemServicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de etapas de ordens de serviço.
    Apenas administradores e operadores podem acessar.
    """
    queryset = EtapaOrdemServico.objects.all()
    serializer_class = EtapaOrdemServicoSerializer
    permission_classes = [IsOperatorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ordem_servico', 'status', 'responsavel']
    ordering_fields = ['ordem', 'data_inicio', 'data_conclusao']


class ItemOrdemServicoListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar itens de ordem de serviço.
    """
    serializer_class = ItemOrdemServicoSerializer
    permission_classes = [IsOperatorOrAdmin]
    
    def get_queryset(self):
        ordem_id = self.kwargs['ordem_id']
        return ItemOrdemServico.objects.filter(ordem_servico_id=ordem_id)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ordem_id = self.kwargs['ordem_id']
        ordem = get_object_or_404(OrdemServico, id=ordem_id)
        
        # Verificar se a ordem está em um estado que permite adicionar itens
        if ordem.status not in ['aguardando', 'aprovada', 'em_andamento']:
            return Response(
                {'detail': 'Não é possível adicionar itens a uma ordem que não está em andamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Adicionar ordem_servico ao contexto do serializer
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
        estoque.save()
        
        # Criar item
        item = serializer.save(ordem_servico=ordem)
        
        # Atualizar valor das peças da ordem
        ordem.valor_pecas = sum(item.subtotal for item in ordem.itens.all())
        ordem.save()
        
        return Response(
            ItemOrdemServicoSerializer(item).data,
            status=status.HTTP_201_CREATED
        )


class ItemOrdemServicoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View para detalhar, atualizar e excluir itens de ordem de serviço.
    """
    serializer_class = ItemOrdemServicoSerializer
    permission_classes = [IsOperatorOrAdmin]
    
    def get_queryset(self):
        ordem_id = self.kwargs['ordem_id']
        return ItemOrdemServico.objects.filter(ordem_servico_id=ordem_id)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        item = self.get_object()
        ordem = item.ordem_servico
        
        # Verificar se a ordem está em um estado que permite atualizar itens
        if ordem.status not in ['aguardando', 'aprovada', 'em_andamento']:
            return Response(
                {'detail': 'Não é possível alterar itens de uma ordem que não está em andamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Liberar estoque reservado
        estoque = Estoque.objects.get(produto=item.produto)
        estoque.quantidade_reservada -= item.quantidade
        
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
        
        # Atualizar valor das peças da ordem
        ordem.valor_pecas = sum(i.subtotal for i in ordem.itens.all())
        ordem.save()
        
        return Response(serializer.data)
    
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        ordem = item.ordem_servico
        
        # Verificar se a ordem está em um estado que permite remover itens
        if ordem.status not in ['aguardando', 'aprovada', 'em_andamento']:
            return Response(
                {'detail': 'Não é possível remover itens de uma ordem que não está em andamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Liberar estoque reservado
        estoque = Estoque.objects.get(produto=item.produto)
        estoque.quantidade_reservada -= item.quantidade
        estoque.save()
        
        # Excluir item
        self.perform_destroy(item)
        
        # Atualizar valor das peças da ordem
        ordem.valor_pecas = sum(i.subtotal for i in ordem.itens.all())
        ordem.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComentarioOrdemServicoListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar comentários de ordem de serviço.
    """
    serializer_class = ComentarioOrdemServicoSerializer
    permission_classes = [IsOperatorOrAdmin]
    
    def get_queryset(self):
        ordem_id = self.kwargs['ordem_id']
        return ComentarioOrdemServico.objects.filter(ordem_servico_id=ordem_id)
    
    def perform_create(self, serializer):
        ordem_id = self.kwargs['ordem_id']
        ordem = get_object_or_404(OrdemServico, id=ordem_id)
        serializer.save(ordem_servico=ordem, usuario=self.request.user)


class AnexoOrdemServicoListCreateView(generics.ListCreateAPIView):
    """
    View para listar e criar anexos de ordem de serviço.
    """
    serializer_class = AnexoOrdemServicoSerializer
    permission_classes = [IsOperatorOrAdmin]
    
    def get_queryset(self):
        ordem_id = self.kwargs['ordem_id']
        return AnexoOrdemServico.objects.filter(ordem_servico_id=ordem_id)
    
    def perform_create(self, serializer):
        ordem_id = self.kwargs['ordem_id']
        ordem = get_object_or_404(OrdemServico, id=ordem_id)
        serializer.save(ordem_servico=ordem, usuario=self.request.user)


class OrdemServicoAprovarView(APIView):
    """
    View para aprovar uma ordem de serviço.
    """
    permission_classes = [IsOperatorOrAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        ordem = get_object_or_404(OrdemServico, id=pk)
        
        # Verificar se a ordem está aguardando aprovação
        if ordem.status != 'aguardando':
            return Response(
                {'detail': 'Não é possível aprovar uma ordem que não está aguardando aprovação.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aprovar ordem
        ordem.status = 'aprovada'
        ordem.data_aprovacao = timezone.now()
        ordem.save()
        
        # Registrar comentário
        ComentarioOrdemServico.objects.create(
            ordem_servico=ordem,
            usuario=request.user,
            texto=f"Ordem de serviço aprovada por {request.user.get_full_name()}"
        )
        
        return Response(
            OrdemServicoDetailSerializer(ordem).data,
            status=status.HTTP_200_OK
        )


class OrdemServicoIniciarView(APIView):
    """
    View para iniciar uma ordem de serviço.
    """
    permission_classes = [IsOperatorOrAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        ordem = get_object_or_404(OrdemServico, id=pk)
        
        # Verificar se a ordem está aprovada
        if ordem.status != 'aprovada':
            return Response(
                {'detail': 'Não é possível iniciar uma ordem que não está aprovada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Iniciar ordem
        ordem.status = 'em_andamento'
        ordem.data_inicio = timezone.now()
        ordem.save()
        
        # Registrar comentário
        ComentarioOrdemServico.objects.create(
            ordem_servico=ordem,
            usuario=request.user,
            texto=f"Ordem de serviço iniciada por {request.user.get_full_name()}"
        )
        
        return Response(
            OrdemServicoDetailSerializer(ordem).data,
            status=status.HTTP_200_OK
        )


class OrdemServicoConcluirView(APIView):
    """
    View para concluir uma ordem de serviço.
    """
    permission_classes = [IsOperatorOrAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        ordem = get_object_or_404(OrdemServico, id=pk)
        
        # Verificar se a ordem está em andamento
        if ordem.status != 'em_andamento':
            return Response(
                {'detail': 'Não é possível concluir uma ordem que não está em andamento.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se todas as etapas estão concluídas
        etapas_pendentes = ordem.etapas.exclude(status='concluida').count()
        if etapas_pendentes > 0:
            return Response(
                {'detail': f'Existem {etapas_pendentes} etapas pendentes.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualizar estoque
        for item in ordem.itens.all():
            # Converter reserva em saída
            estoque = Estoque.objects.get(produto=item.produto)
            estoque.quantidade_reservada -= item.quantidade
            estoque.quantidade_atual -= item.quantidade
            estoque.save()
            
            # Registrar movimentação
            MovimentacaoEstoque.objects.create(
                produto=item.produto,
                tipo='saida',
                origem='ordem_servico',
                quantidade=item.quantidade,
                valor_unitario=item.preco_unitario,
                documento=f"OS #{ordem.numero}",
                usuario=request.user,
                referencia_id=ordem.id,
                referencia_tipo='ordem_servico'
            )
        
        # Concluir ordem
        ordem.status = 'concluida'
        ordem.data_conclusao = timezone.now()
        ordem.save()
        
        # Registrar comentário
        ComentarioOrdemServico.objects.create(
            ordem_servico=ordem,
            usuario=request.user,
            texto=f"Ordem de serviço concluída por {request.user.get_full_name()}"
        )
        
        return Response(
            OrdemServicoDetailSerializer(ordem).data,
            status=status.HTTP_200_OK
        )


class OrdemServicoCancelarView(APIView):
    """
    View para cancelar uma ordem de serviço.
    """
    permission_classes = [IsOperatorOrAdmin]
    
    @transaction.atomic
    def post(self, request, pk):
        ordem = get_object_or_404(OrdemServico, id=pk)
        
        # Verificar se a ordem já está cancelada
        if ordem.status == 'cancelada':
            return Response(
                {'detail': 'Esta ordem já está cancelada.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = OrdemServicoCancelarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Liberar estoque reservado
        for item in ordem.itens.all():
            estoque = Estoque.objects.get(produto=item.produto)
            estoque.quantidade_reservada -= item.quantidade
            estoque.save()
        
        # Cancelar ordem
        ordem.status = 'cancelada'
        ordem.data_cancelamento = timezone.now()
        ordem.motivo_cancelamento = serializer.validated_data['motivo']
        ordem.save()
        
        # Registrar comentário
        ComentarioOrdemServico.objects.create(
            ordem_servico=ordem,
            usuario=request.user,
            texto=f"Ordem de serviço cancelada por {request.user.get_full_name()}. Motivo: {serializer.validated_data['motivo']}"
        )
        
        return Response(
            OrdemServicoDetailSerializer(ordem).data,
            status=status.HTTP_200_OK
        )


class PainelIndustrialView(APIView):
    """
    View para o painel industrial (telão).
    Acesso público com token.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Verificar token (em produção)
        token = request.query_params.get('token')
        if not token:
            return Response(
                {'detail': 'Token não informado.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Em ambiente de desenvolvimento, aceitar qualquer token
        # Em produção, verificar token válido
        
        # Obter ordens em andamento
        ordens_andamento = OrdemServico.objects.filter(status='em_andamento')
        
        # Obter ordens aguardando aprovação
        ordens_aguardando = OrdemServico.objects.filter(status='aguardando')
        
        # Obter ordens concluídas hoje
        hoje = timezone.now().date()
        ordens_concluidas = OrdemServico.objects.filter(
            status='concluida',
            data_conclusao__date=hoje
        )
        
        # Obter etapas em andamento
        etapas_andamento = EtapaOrdemServico.objects.filter(
            status='em_andamento',
            ordem_servico__status='em_andamento'
        )
        
        return Response({
            'ordens_andamento': OrdemServicoListSerializer(ordens_andamento, many=True).data,
            'ordens_aguardando': OrdemServicoListSerializer(ordens_aguardando, many=True).data,
            'ordens_concluidas': OrdemServicoListSerializer(ordens_concluidas, many=True).data,
            'etapas_andamento': EtapaOrdemServicoSerializer(etapas_andamento, many=True).data,
            'estatisticas': {
                'total_andamento': ordens_andamento.count(),
                'total_aguardando': ordens_aguardando.count(),
                'total_concluidas_hoje': ordens_concluidas.count(),
                'tempo_medio_conclusao': '2h 30min'  # Exemplo, calcular real em produção
            }
        })


class RelatorioOrdensServicoView(APIView):
    """
    View para relatório de ordens de serviço.
    """
    permission_classes = [IsOperatorOrAdmin]
    
    def get(self, request):
        # Parâmetros de filtro
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        status = request.query_params.get('status')
        tecnico_id = request.query_params.get('tecnico_id')
        cliente_id = request.query_params.get('cliente_id')
        
        # Base da query
        queryset = OrdemServico.objects.all()
        
        # Aplicar filtros
        if data_inicio:
            queryset = queryset.filter(data_abertura__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_abertura__lte=data_fim)
        if status:
            queryset = queryset.filter(status=status)
        if tecnico_id:
            queryset = queryset.filter(tecnico_id=tecnico_id)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        # Calcular totais
        total_ordens = queryset.count()
        total_valor = sum(ordem.valor_total for ordem in queryset)
        
        # Agrupar por status
        ordens_por_status = {}
        for ordem in queryset:
            status_display = ordem.get_status_display()
            if status_display not in ordens_por_status:
                ordens_por_status[status_display] = {
                    'quantidade': 0,
                    'valor_total': 0
                }
            ordens_por_status[status_display]['quantidade'] += 1
            ordens_por_status[status_display]['valor_total'] += ordem.valor_total
        
        return Response({
            'total_ordens': total_ordens,
            'total_valor': total_valor,
            'ordens_por_status': ordens_por_status,
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim or timezone.now().date().isoformat()
            }
        })
