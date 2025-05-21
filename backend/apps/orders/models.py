from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class StatusPedido(models.TextChoices):
    CARRINHO = 'carrinho', _('Carrinho')
    AGUARDANDO_PAGAMENTO = 'aguardando_pagamento', _('Aguardando Pagamento')
    PAGO = 'pago', _('Pago')
    EM_PREPARACAO = 'em_preparacao', _('Em Preparação')
    ENVIADO = 'enviado', _('Enviado')
    ENTREGUE = 'entregue', _('Entregue')
    CANCELADO = 'cancelado', _('Cancelado')

class MetodoPagamento(models.TextChoices):
    CARTAO_CREDITO = 'cartao_credito', _('Cartão de Crédito')
    BOLETO = 'boleto', _('Boleto')
    PIX = 'pix', _('PIX')
    TRANSFERENCIA = 'transferencia', _('Transferência Bancária')

class Order(models.Model):
    """
    Modelo para pedidos.
    """
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Em processamento'),
        ('completed', 'Concluído'),
        ('canceled', 'Cancelado'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    # Informações de pagamento
    payment_method = models.CharField(
        _('método de pagamento'),
        max_length=20,
        choices=MetodoPagamento.choices,
        null=True,
        blank=True
    )
    payment_date = models.DateTimeField(_('data de pagamento'), null=True, blank=True)
    
    # Informações de entrega
    shipping_address = models.CharField(_('endereço de entrega'), max_length=255, null=True, blank=True)
    shipping_city = models.CharField(_('cidade'), max_length=100, null=True, blank=True)
    shipping_state = models.CharField(_('estado'), max_length=2, null=True, blank=True)
    shipping_zip = models.CharField(_('CEP'), max_length=10, null=True, blank=True)
    shipping_date = models.DateTimeField(_('data de envio'), null=True, blank=True)
    delivery_date = models.DateTimeField(_('data de entrega'), null=True, blank=True)
    tracking_code = models.CharField(_('código de rastreamento'), max_length=50, null=True, blank=True)
    
    # Valores adicionais
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(_('desconto'), max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(_('frete'), max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('pedido')
        verbose_name_plural = _('pedidos')
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.customer.get_full_name()}"
    
    def calculate_total(self):
        """
        Calcula o total do pedido com base nos itens, desconto e frete.
        """
        # Calcular subtotal
        self.subtotal = sum(item.subtotal for item in self.items.all())
        
        # Calcular total
        self.total = self.subtotal - self.discount + self.shipping_cost
        
        self.save(update_fields=['subtotal', 'total'])
        return self.total

    def verificar_estoque(self):
        """
        Verifica se há estoque suficiente para todos os itens do pedido.
        """
        for item in self.items.all():
            estoque = Estoque.objects.filter(produto=item.product).first()
            if estoque and estoque.quantidade_disponivel < item.quantity:
                return False
        return True
    
    def add_item(self, product, quantity=1, price=None):
        """
        Adiciona um item ao pedido ou atualiza a quantidade se já existir.
        """
        if not price:
            price = product.preco
            
        item, created = OrderItem.objects.get_or_create(
            order=self,
            product=product,
            defaults={
                'quantity': quantity,
                'price': price
            }
        )
        
        if not created:
            item.quantity += quantity
            item.save()
            
        self.calculate_total()
        return item
    
    def remove_item(self, product):
        """
        Remove um item do pedido.
        """
        try:
            item = self.items.get(product=product)
            item.delete()
            self.calculate_total()
            return True
        except OrderItem.DoesNotExist:
            return False
    
    def update_item_quantity(self, product, quantity):
        """
        Atualiza a quantidade de um item no pedido.
        """
        try:
            item = self.items.get(product=product)
            if quantity <= 0:
                return self.remove_item(product)
            
            item.quantity = quantity
            item.save()
            self.calculate_total()
            return True
        except OrderItem.DoesNotExist:
            return False
    
    def finalize_order(self):
        """
        Finaliza o pedido, alterando o status para aguardando pagamento.
        """
        if self.status == 'pending':
            self.status = 'processing'
            self.save()
            return True
        return False
    
    def mark_as_paid(self, payment_method):
        """
        Registra o pagamento do pedido.
        """
        if self.status == 'processing':
            self.status = 'completed'
            self.payment_method = payment_method
            self.payment_date = timezone.now()
            self.save()
            return True
        return False
    
    def cancel(self):
        """
        Cancela o pedido.
        """
        if self.status not in ['completed', 'canceled']:
            self.status = 'canceled'
            self.save()
            return True
        return False


class OrderItem(models.Model):
    """
    Modelo para itens de pedido.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Produto', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
        unique_together = ('order', 'product')
        verbose_name = _('item de pedido')
        verbose_name_plural = _('itens de pedido')
        
    def __str__(self):
        return f"{self.quantity}x {self.product.nome}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para atualizar o total do pedido.
        """
        super().save(*args, **kwargs)
        self.order.calculate_total()
