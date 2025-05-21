from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.serializers import ProdutoSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer para itens de pedido.
    """
    product_details = ProdutoSerializer(source='product', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer para pedidos.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'status', 'created_at', 'updated_at', 'total', 'notes', 'items']
        read_only_fields = ['created_at', 'updated_at']
