from django.db import models
from django.utils import timezone

class Employee(models.Model):
    """
    Modelo para funcionários.
    """
    DEPARTMENT_CHOICES = (
        ('admin', 'Administrativo'),
        ('sales', 'Vendas'),
        ('technical', 'Técnico'),
        ('support', 'Suporte'),
        ('management', 'Gerência'),
    )
    
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='employee_profile')
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    # Documentos e informações adicionais
    cpf = models.CharField(max_length=14, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"
