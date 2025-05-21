from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Produto
from apps.accounts.models import User


class OrdemServico(models.Model):
    """
    Modelo para ordens de serviço.
    """
    STATUS_CHOICES = (
        ('aguardando', 'Aguardando Aprovação'),
        ('aprovada', 'Aprovada'),
        ('em_andamento', 'Em Andamento'),
        ('pausada', 'Pausada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    )
    
    PRIORIDADE_CHOICES = (
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    )
    
    numero = models.CharField(_('número'), max_length=20, unique=True)
    cliente = models.ForeignKey('pos.Cliente', on_delete=models.PROTECT, related_name='ordens_servico', verbose_name=_('cliente'))
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ordens_servico_responsavel', verbose_name=_('responsável'))
    tecnico = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ordens_servico_tecnico', verbose_name=_('técnico'), null=True, blank=True)
    data_abertura = models.DateTimeField(_('data de abertura'), auto_now_add=True)
    data_aprovacao = models.DateTimeField(_('data de aprovação'), null=True, blank=True)
    data_inicio = models.DateTimeField(_('data de início'), null=True, blank=True)
    data_conclusao = models.DateTimeField(_('data de conclusão'), null=True, blank=True)
    data_cancelamento = models.DateTimeField(_('data de cancelamento'), null=True, blank=True)
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='aguardando')
    prioridade = models.CharField(_('prioridade'), max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    
    # Descrições
    descricao_problema = models.TextField(_('descrição do problema'))
    descricao_servico = models.TextField(_('descrição do serviço'), blank=True, null=True)
    observacoes = models.TextField(_('observações'), blank=True, null=True)
    
    # Valores
    valor_servico = models.DecimalField(_('valor do serviço'), max_digits=10, decimal_places=2, default=0)
    valor_pecas = models.DecimalField(_('valor das peças'), max_digits=10, decimal_places=2, default=0)
    valor_total = models.DecimalField(_('valor total'), max_digits=10, decimal_places=2, default=0)
    
    # Campos adicionais
    garantia = models.PositiveIntegerField(_('garantia (dias)'), default=30)
    motivo_cancelamento = models.TextField(_('motivo do cancelamento'), blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('ordem de serviço')
        verbose_name_plural = _('ordens de serviço')
        ordering = ['-data_abertura']

    def __str__(self):
        return f"OS #{self.numero} - {self.cliente.nome}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular o valor total.
        """
        self.valor_total = self.valor_servico + self.valor_pecas
        
        # Gerar número da OS se for uma nova OS
        if not self.numero:
            ultimo_numero = OrdemServico.objects.order_by('-id').first()
            if ultimo_numero:
                ultimo_id = ultimo_numero.id
            else:
                ultimo_id = 0
            self.numero = f"OS{ultimo_id + 1:06d}"
        
        super().save(*args, **kwargs)


class ItemOrdemServico(models.Model):
    """
    Modelo para itens (peças) utilizados em ordens de serviço.
    """
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='itens', verbose_name=_('ordem de serviço'))
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_os', verbose_name=_('produto'))
    quantidade = models.DecimalField(_('quantidade'), max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(_('preço unitário'), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('item de ordem de serviço')
        verbose_name_plural = _('itens de ordem de serviço')
        ordering = ['id']

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular o subtotal.
        """
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)


class EtapaOrdemServico(models.Model):
    """
    Modelo para etapas de execução de ordens de serviço.
    """
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    )
    
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='etapas', verbose_name=_('ordem de serviço'))
    nome = models.CharField(_('nome'), max_length=100)
    descricao = models.TextField(_('descrição'), blank=True, null=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pendente')
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='etapas_os', verbose_name=_('responsável'), null=True, blank=True)
    ordem = models.PositiveIntegerField(_('ordem'), default=0)
    
    data_inicio = models.DateTimeField(_('data de início'), null=True, blank=True)
    data_conclusao = models.DateTimeField(_('data de conclusão'), null=True, blank=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('etapa de ordem de serviço')
        verbose_name_plural = _('etapas de ordem de serviço')
        ordering = ['ordem_servico', 'ordem']

    def __str__(self):
        return f"{self.nome} - OS #{self.ordem_servico.numero}"


class ComentarioOrdemServico(models.Model):
    """
    Modelo para comentários em ordens de serviço.
    """
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='comentarios', verbose_name=_('ordem de serviço'))
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comentarios_os', verbose_name=_('usuário'))
    texto = models.TextField(_('texto'))
    data = models.DateTimeField(_('data'), auto_now_add=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('comentário de ordem de serviço')
        verbose_name_plural = _('comentários de ordem de serviço')
        ordering = ['-data']

    def __str__(self):
        return f"Comentário de {self.usuario.get_full_name()} em {self.data}"


class AnexoOrdemServico(models.Model):
    """
    Modelo para anexos em ordens de serviço.
    """
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name='anexos', verbose_name=_('ordem de serviço'))
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='anexos_os', verbose_name=_('usuário'))
    arquivo = models.FileField(_('arquivo'), upload_to='ordens_servico/anexos/')
    nome = models.CharField(_('nome'), max_length=100)
    descricao = models.TextField(_('descrição'), blank=True, null=True)
    data = models.DateTimeField(_('data'), auto_now_add=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('anexo de ordem de serviço')
        verbose_name_plural = _('anexos de ordem de serviço')
        ordering = ['-data']

    def __str__(self):
        return f"Anexo {self.nome} - OS #{self.ordem_servico.numero}"
