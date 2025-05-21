from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from django.shortcuts import get_object_or_404

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gerenciar pedidos.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """
        Filtra os pedidos com base no usuário.
        Administradores veem todos os pedidos, clientes veem apenas os seus.
        """
        user = self.request.user
        if user.is_admin:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
    def perform_create(self, serializer):
        """
        Associa o usuário atual ao pedido ao criar.
        """
        serializer.save(customer=self.request.user)

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
        return Order.objects.filter(customer=self.request.user)
