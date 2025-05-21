from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Produto


class Estoque(models.Model):
    """
    Modelo para controle de estoque de produtos.
    """
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name='estoque', verbose_name=_('produto'))
    quantidade_atual = models.DecimalField(_('quantidade atual'), max_digits=10, decimal_places=2, default=0)
    quantidade_reservada = models.DecimalField(_('quantidade reservada'), max_digits=10, decimal_places=2, default=0)
    quantidade_disponivel = models.DecimalField(_('quantidade disponível'), max_digits=10, decimal_places=2, default=0)
    ultima_atualizacao = models.DateTimeField(_('última atualização'), auto_now=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('estoque')
        verbose_name_plural = _('estoques')
        ordering = ['produto__nome']

    def __str__(self):
        return f"Estoque de {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular a quantidade disponível.
        """
        self.quantidade_disponivel = max(0, self.quantidade_atual - self.quantidade_reservada)
        super().save(*args, **kwargs)
    
    @property
    def status(self):
        """
        Retorna o status do estoque com base na quantidade disponível e estoque mínimo.
        """
        if self.quantidade_disponivel <= 0:
            return 'esgotado'
        elif self.quantidade_disponivel < self.produto.estoque_minimo:
            return 'baixo'
        else:
            return 'normal'


class MovimentacaoEstoque(models.Model):
    """
    Modelo para registrar movimentações de estoque.
    """
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
        ('reserva', 'Reserva'),
        ('cancelamento', 'Cancelamento de Reserva'),
    )
    
    ORIGEM_CHOICES = (
        ('compra', 'Compra'),
        ('venda', 'Venda'),
        ('devolucao', 'Devolução'),
        ('ajuste_manual', 'Ajuste Manual'),
        ('ordem_servico', 'Ordem de Serviço'),
        ('pedido_online', 'Pedido Online'),
    )
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='movimentacoes', verbose_name=_('produto'))
    tipo = models.CharField(_('tipo'), max_length=20, choices=TIPO_CHOICES)
    origem = models.CharField(_('origem'), max_length=20, choices=ORIGEM_CHOICES)
    quantidade = models.DecimalField(_('quantidade'), max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(_('valor unitário'), max_digits=10, decimal_places=2, blank=True, null=True)
    documento = models.CharField(_('documento'), max_length=50, blank=True, null=True)
    observacao = models.TextField(_('observação'), blank=True, null=True)
    usuario = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentacoes_estoque', verbose_name=_('usuário'))
    data_movimentacao = models.DateTimeField(_('data da movimentação'), auto_now_add=True)
    
    # Campos para rastreabilidade
    referencia_id = models.PositiveIntegerField(_('ID de referência'), blank=True, null=True)
    referencia_tipo = models.CharField(_('tipo de referência'), max_length=50, blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('movimentação de estoque')
        verbose_name_plural = _('movimentações de estoque')
        ordering = ['-data_movimentacao']

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade} {self.produto.unidade} de {self.produto.nome}"
