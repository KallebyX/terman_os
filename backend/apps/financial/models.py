from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    """
    Modelo para transações financeiras.
    """
    TYPE_CHOICES = (
        ('income', 'Receita'),
        ('expense', 'Despesa'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('completed', 'Concluída'),
        ('canceled', 'Cancelada'),
    )
    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relacionamentos opcionais
    customer = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.get_type_display()} - {self.description} - R$ {self.amount}"
