from rest_framework import serializers
from .models import Order, OrderItem, MetodoPagamento, StatusPedido
from apps.products.serializers import ProdutoSerializer
from apps.products.models import Produto
from django.db import transaction
from django.utils.translation import gettext_lazy as _

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer para itens de pedido.
    """
    product_details = ProdutoSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_details', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']
    
    def validate_quantity(self, value):
        """
        Valida se a quantidade é maior que zero.
        """
        if value <= 0:
            raise serializers.ValidationError(_("A quantidade deve ser maior que zero."))
        return value
    
    def validate_product(self, value):
        """
        Valida se o produto está disponível.
        """
        if not hasattr(value, 'disponivel') or not value.disponivel:
            raise serializers.ValidationError(_("Este produto não está disponível."))
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer para pedidos.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'status', 'status_display', 
            'created_at', 'updated_at', 'payment_date', 'shipping_date', 'delivery_date',
            'payment_method', 'payment_method_display', 'tracking_code', 'notes',
            'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip',
            'subtotal', 'discount', 'shipping_cost', 'total', 'items'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'payment_date', 
            'shipping_date', 'delivery_date', 'subtotal', 'total'
        ]


class AddItemSerializer(serializers.Serializer):
    """
    Serializer para adicionar um item ao pedido.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate_product_id(self, value):
        """
        Valida se o produto existe.
        """
        try:
            product = Produto.objects.get(id=value)
            if not hasattr(product, 'disponivel') or not product.disponivel:
                raise serializers.ValidationError(_("Este produto não está disponível."))
            return value
        except Produto.DoesNotExist:
            raise serializers.ValidationError(_("Produto não encontrado."))


class UpdateItemQuantitySerializer(serializers.Serializer):
    """
    Serializer para atualizar a quantidade de um item no pedido.
    """
    quantity = serializers.IntegerField(min_value=0)


class FinalizeOrderSerializer(serializers.Serializer):
    """
    Serializer para finalizar um pedido.
    """
    shipping_address = serializers.CharField(max_length=255)
    shipping_city = serializers.CharField(max_length=100)
    shipping_state = serializers.CharField(max_length=2)
    shipping_zip = serializers.CharField(max_length=10)
    notes = serializers.CharField(required=False, allow_blank=True)


class PaymentSerializer(serializers.Serializer):
    """
    Serializer para registrar o pagamento de um pedido.
    """
    payment_method = serializers.ChoiceField(choices=MetodoPagamento.choices)


class ShippingSerializer(serializers.Serializer):
    """
    Serializer para registrar o envio de um pedido.
    """
    tracking_code = serializers.CharField(max_length=50, required=False, allow_blank=True)


class CartSerializer(serializers.Serializer):
    """
    Serializer para criar um novo carrinho.
    """
    customer_id = serializers.IntegerField(required=False)
    
    @transaction.atomic
    def create(self, validated_data):
        """
        Cria um novo carrinho para o cliente.
        """
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        customer_id = validated_data.get('customer_id')
        try:
            customer = User.objects.get(id=customer_id)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Cliente não encontrado."))
        
        # Verificar se já existe um carrinho ativo para o cliente
        existing_cart = Order.objects.filter(
            customer=customer, 
            status='pending'
        ).first()
        
        if existing_cart:
            return existing_cart
        
        # Criar novo carrinho
        return Order.objects.create(customer=customer, status='pending')
