from rest_framework import viewsets, generics, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, OrderItemSerializer, AddItemSerializer,
    UpdateItemQuantitySerializer, FinalizeOrderSerializer,
    PaymentSerializer, ShippingSerializer, CartSerializer
)
from apps.products.models import Produto
from apps.inventory.models import Estoque, MovimentacaoEstoque

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas o proprietário do pedido
    ou administradores/vendedores possam acessá-lo.
    """
    
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário é o proprietário do pedido
        if hasattr(obj, 'customer'):
            return obj.customer == request.user or request.user.is_admin or request.user.is_seller
        
        # Para OrderItem, verificar o proprietário do pedido
        if hasattr(obj, 'order'):
            return obj.order.customer == request.user or request.user.is_admin or request.user.is_seller
        
        return False


class IsSellerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir acesso apenas a vendedores e administradores.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_seller)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar pedidos.
    """
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method']
    search_fields = ['id', 'customer__email', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filtra os pedidos com base no usuário.
        Administradores veem todos os pedidos, clientes veem apenas os seus.
        """
        user = self.request.user
        if user.is_admin or user.is_seller:
            return Order.objects.all().select_related('customer').prefetch_related('items', 'items__product')
        return Order.objects.filter(customer=user).select_related('customer').prefetch_related('items', 'items__product')
    
    def get_permissions(self):
        """
        Define as permissões com base na ação.
        """
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Associa o usuário atual ao pedido ao criar e verifica o estoque.
        """
        order = serializer.save(customer=self.request.user)
        if not order.verificar_estoque():
            raise serializers.ValidationError("Estoque insuficiente para um ou mais itens do pedido.")
    
    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """
        Adiciona um item ao pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido está no status de pendente
        if order.status != 'pending':
            return Response(
                {"detail": "Só é possível adicionar itens a um pedido pendente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AddItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        try:
            product = Produto.objects.get(id=product_id)
            
            # Verificar se o produto está ativo
            if not product.ativo:
                return Response(
                    {"detail": "Este produto não está disponível para venda."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verificar disponibilidade em estoque
            estoque = Estoque.objects.filter(produto=product).first()
            if estoque and estoque.quantidade_disponivel < quantity:
                return Response(
                    {"detail": f"Quantidade insuficiente em estoque. Disponível: {estoque.quantidade_disponivel}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reservar estoque
            if estoque:
                estoque.quantidade_reservada += quantity
                estoque.save()
            
            # Adicionar item ao pedido
            order.add_item(product, quantity)
            
            return Response(OrderSerializer(order).data)
        
        except Produto.DoesNotExist:
            return Response(
                {"detail": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        """
        Remove um item do pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido está no status de pendente
        if order.status != 'pending':
            return Response(
                {"detail": "Só é possível remover itens de um pedido pendente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {"detail": "É necessário informar o ID do produto."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Produto.objects.get(id=product_id)
            
            # Remover item do pedido
            if order.remove_item(product):
                return Response(OrderSerializer(order).data)
            else:
                return Response(
                    {"detail": "Item não encontrado no pedido."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        except Produto.DoesNotExist:
            return Response(
                {"detail": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """
        Atualiza a quantidade de um item no pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido está no status de pendente
        if order.status != 'pending':
            return Response(
                {"detail": "Só é possível atualizar itens de um pedido pendente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {"detail": "É necessário informar o ID do produto."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UpdateItemQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        quantity = serializer.validated_data['quantity']
        
        try:
            product = Produto.objects.get(id=product_id)
            
            # Verificar disponibilidade em estoque
            if quantity > 0:
                estoque = Estoque.objects.filter(produto=product).first()
                if estoque and estoque.quantidade_disponivel < quantity:
                    return Response(
                        {"detail": f"Quantidade insuficiente em estoque. Disponível: {estoque.quantidade_disponivel}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Atualizar quantidade do item
            if order.update_item_quantity(product, quantity):
                return Response(OrderSerializer(order).data)
            else:
                return Response(
                    {"detail": "Item não encontrado no pedido."},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        except Produto.DoesNotExist:
            return Response(
                {"detail": "Produto não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        """
        Finaliza o pedido, alterando o status para processando.
        """
        order = self.get_object()
        
        # Verificar se o pedido está no status de pendente
        if order.status != 'pending':
            return Response(
                {"detail": "Só é possível finalizar um pedido pendente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar se o pedido tem itens
        if not order.items.exists():
            return Response(
                {"detail": "Não é possível finalizar um pedido sem itens."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar estoque
        if not order.verificar_estoque():
            return Response(
                {"detail": "Estoque insuficiente para um ou mais itens do pedido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FinalizeOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Atualizar informações de entrega
        for field in ['shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'notes']:
            if field in serializer.validated_data:
                setattr(order, field, serializer.validated_data[field])
        
        # Finalizar pedido
        if order.finalize_order():
            order.save()
            return Response(OrderSerializer(order).data)
        else:
            return Response(
                {"detail": "Não foi possível finalizar o pedido."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSellerOrAdmin])
    def mark_as_paid(self, request, pk=None):
        """
        Registra o pagamento do pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido está processando
        if order.status != 'processing':
            return Response(
                {"detail": "Só é possível registrar pagamento de um pedido em processamento."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payment_method = serializer.validated_data['payment_method']
        
        # Verificar estoque antes de confirmar pagamento
        for item in order.items.all():
            estoque = Estoque.objects.filter(produto=item.product).first()
            if not estoque or estoque.quantidade_disponivel < item.quantity:
                return Response(
                    {"detail": f"Estoque insuficiente para o produto {item.product.nome}. Por favor, atualize o pedido."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Registrar pagamento
        if order.mark_as_paid(payment_method):
            # Baixar estoque
            with transaction.atomic():
                for item in order.items.all():
                    estoque = Estoque.objects.filter(produto=item.product).first()
                    if estoque:
                        # Atualizar estoque
                        estoque.quantidade_atual -= item.quantity
                        estoque.save()
                        
                        # Registrar movimentação de saída
                        MovimentacaoEstoque.objects.create(
                            produto=item.product,
                            tipo='saida',
                            origem='venda',
                            quantidade=item.quantity,
                            valor_unitario=item.price,
                            documento=f"Pedido #{order.id}",
                            observacao=f"Venda para {order.customer.get_full_name()}",
                            usuario=request.user,
                            referencia_id=order.id,
                            referencia_tipo='pedido'
                        )
            
            return Response(OrderSerializer(order).data)
        else:
            return Response(
                {"detail": "Não foi possível registrar o pagamento."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSellerOrAdmin])
    def ship(self, request, pk=None):
        """
        Registra o envio do pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido está completo (pago)
        if order.status != 'completed':
            return Response(
                {"detail": "Só é possível registrar envio de um pedido completo."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ShippingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tracking_code = serializer.validated_data.get('tracking_code')
        
        # Registrar envio
        order.shipping_date = timezone.now()
        if tracking_code:
            order.tracking_code = tracking_code
        order.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsSellerOrAdmin])
    def deliver(self, request, pk=None):
        """
        Registra a entrega do pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido foi enviado
        if not order.shipping_date:
            return Response(
                {"detail": "Só é possível registrar entrega de um pedido enviado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Registrar entrega
        order.delivery_date = timezone.now()
        order.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancela o pedido.
        """
        order = self.get_object()
        
        # Verificar se o pedido pode ser cancelado
        if order.status in ['completed', 'canceled'] and order.delivery_date:
            return Response(
                {"detail": "Não é possível cancelar um pedido entregue ou já cancelado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Se o pedido já estiver pago, apenas admin pode cancelar
        if order.status == 'completed' and not request.user.is_admin:
            return Response(
                {"detail": "Apenas administradores podem cancelar pedidos pagos."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Cancelar pedido
        if order.cancel():
            # Se o pedido estava pago, devolver ao estoque
            if order.status == 'completed':
                with transaction.atomic():
                    for item in order.items.all():
                        estoque = Estoque.objects.filter(produto=item.product).first()
                        if estoque:
                            # Atualizar estoque
                            estoque.quantidade_atual += item.quantity
                            estoque.save()
                            
                            # Registrar movimentação de entrada (devolução)
                            MovimentacaoEstoque.objects.create(
                                produto=item.product,
                                tipo='entrada',
                                origem='devolucao',
                                quantidade=item.quantity,
                                valor_unitario=item.price,
                                documento=f"Pedido #{order.id}",
                                observacao=f"Cancelamento de pedido para {order.customer.get_full_name()}",
                                usuario=request.user,
                                referencia_id=order.id,
                                referencia_tipo='pedido'
                            )
            # Se o pedido estava pendente, liberar reservas
            elif order.status == 'pending':
                with transaction.atomic():
                    for item in order.items.all():
                        estoque = Estoque.objects.filter(produto=item.product).first()
                        if estoque:
                            # Liberar quantidade reservada
                            estoque.quantidade_reservada -= item.quantity
                            estoque.save()
                            
                            # Registrar movimentação
                            MovimentacaoEstoque.objects.create(
                                produto=item.product,
                                tipo='cancelamento',
                                origem='pedido_cancelado',
                                quantidade=item.quantity,
                                valor_unitario=item.price,
                                documento=f"Pedido #{order.id}",
                                observacao=f"Cancelamento de reserva para {order.customer.get_full_name()}",
                                usuario=request.user,
                                referencia_id=order.id,
                                referencia_tipo='pedido'
                            )
            
            return Response(OrderSerializer(order).data)
        else:
            return Response(
                {"detail": "Não foi possível cancelar o pedido."},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def create_cart(self, request):
        """
        Cria um novo carrinho para o cliente.
        """
        # Se não for admin, usar o próprio usuário como cliente
        if not request.user.is_admin:
            data = {'customer_id': request.user.id}
        else:
            data = request.data
        
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        cart = serializer.create(serializer.validated_data)
        return Response(OrderSerializer(cart).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """
        Retorna o carrinho ativo do cliente.
        """
        cart = Order.objects.filter(
            customer=request.user, 
            status='pending'
        ).first()
        
        if cart:
            return Response(OrderSerializer(cart).data)
        else:
            # Criar novo carrinho
            cart = Order.objects.create(customer=request.user, status='pending')
            return Response(OrderSerializer(cart).data)
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """
        Retorna os pedidos do cliente (excluindo carrinhos).
        """
        orders = Order.objects.filter(
            customer=request.user
        ).exclude(
            status='pending'
        ).order_by('-created_at')
        
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class MyOrdersView(generics.ListAPIView):
    """
    API endpoint para listar os pedidos do usuário atual.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Retorna apenas os pedidos do usuário atual.
        """
        return Order.objects.filter(customer=self.request.user).exclude(status='pending')
