from django.db import models
from django.utils import timezone

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
    
    customer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Pedido #{self.id} - {self.customer.name}"


class OrderItem(models.Model):
    """
    Modelo para itens de pedido.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f"{self.quantity}x {self.product.nome}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity
