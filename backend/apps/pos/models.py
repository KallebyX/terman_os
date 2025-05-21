from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.products.models import Produto
from apps.accounts.models import User


class Cliente(models.Model):
    """
    Modelo para clientes (pessoas físicas e jurídicas).
    """
    TIPO_CHOICES = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    )
    
    tipo = models.CharField(_('tipo'), max_length=2, choices=TIPO_CHOICES)
    nome = models.CharField(_('nome'), max_length=200)
    email = models.EmailField(_('email'), blank=True, null=True)
    telefone = models.CharField(_('telefone'), max_length=20, blank=True, null=True)
    celular = models.CharField(_('celular'), max_length=20, blank=True, null=True)
    
    # Campos para Pessoa Física
    cpf = models.CharField(_('CPF'), max_length=14, blank=True, null=True, unique=True)
    rg = models.CharField(_('RG'), max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(_('data de nascimento'), blank=True, null=True)
    
    # Campos para Pessoa Jurídica
    razao_social = models.CharField(_('razão social'), max_length=200, blank=True, null=True)
    cnpj = models.CharField(_('CNPJ'), max_length=18, blank=True, null=True, unique=True)
    inscricao_estadual = models.CharField(_('inscrição estadual'), max_length=20, blank=True, null=True)
    inscricao_municipal = models.CharField(_('inscrição municipal'), max_length=20, blank=True, null=True)
    contato = models.CharField(_('contato'), max_length=100, blank=True, null=True)
    
    # Endereço
    endereco = models.CharField(_('endereço'), max_length=255, blank=True, null=True)
    numero = models.CharField(_('número'), max_length=10, blank=True, null=True)
    complemento = models.CharField(_('complemento'), max_length=100, blank=True, null=True)
    bairro = models.CharField(_('bairro'), max_length=100, blank=True, null=True)
    cidade = models.CharField(_('cidade'), max_length=100, blank=True, null=True)
    estado = models.CharField(_('estado'), max_length=2, blank=True, null=True)
    cep = models.CharField(_('CEP'), max_length=10, blank=True, null=True)
    
    # Campos adicionais
    observacoes = models.TextField(_('observações'), blank=True, null=True)
    limite_credito = models.DecimalField(_('limite de crédito'), max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(_('ativo'), default=True)
    
    # Relacionamento com usuário (opcional)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='cliente')
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('cliente')
        verbose_name_plural = _('clientes')
        ordering = ['nome']

    def __str__(self):
        if self.tipo == 'pj' and self.razao_social:
            return f"{self.nome} ({self.razao_social})"
        return self.nome
    
    @property
    def documento(self):
        """
        Retorna o documento principal do cliente (CPF ou CNPJ).
        """
        if self.tipo == 'pf':
            return self.cpf
        return self.cnpj
    
    @property
    def tipo_display(self):
        """
        Retorna o tipo de cliente formatado.
        """
        return dict(self.TIPO_CHOICES).get(self.tipo)


class Venda(models.Model):
    """
    Modelo para vendas (PDV).
    """
    STATUS_CHOICES = (
        ('aberta', 'Aberta'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    )
    
    TIPO_CHOICES = (
        ('balcao', 'Balcão'),
        ('entrega', 'Entrega'),
        ('ordem_servico', 'Ordem de Serviço'),
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='vendas', verbose_name=_('cliente'))
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='vendas_realizadas', verbose_name=_('vendedor'))
    data_venda = models.DateTimeField(_('data da venda'), auto_now_add=True)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='aberta')
    tipo = models.CharField(_('tipo'), max_length=20, choices=TIPO_CHOICES, default='balcao')
    
    # Valores
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(_('desconto'), max_digits=10, decimal_places=2, default=0)
    acrescimo = models.DecimalField(_('acréscimo'), max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(_('total'), max_digits=10, decimal_places=2, default=0)
    
    # Campos adicionais
    observacoes = models.TextField(_('observações'), blank=True, null=True)
    data_finalizacao = models.DateTimeField(_('data de finalização'), blank=True, null=True)
    data_cancelamento = models.DateTimeField(_('data de cancelamento'), blank=True, null=True)
    motivo_cancelamento = models.TextField(_('motivo do cancelamento'), blank=True, null=True)
    
    # Campos para nota fiscal
    nfe_emitida = models.BooleanField(_('NFe emitida'), default=False)
    nfe_numero = models.CharField(_('número da NFe'), max_length=20, blank=True, null=True)
    nfe_chave = models.CharField(_('chave da NFe'), max_length=44, blank=True, null=True)
    nfe_data = models.DateTimeField(_('data da NFe'), blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('venda')
        verbose_name_plural = _('vendas')
        ordering = ['-data_venda']

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome}"
    
    def calcular_total(self):
        """
        Calcula o total da venda.
        """
        self.subtotal = sum(item.subtotal for item in self.itens.all())
        self.total = self.subtotal - self.desconto + self.acrescimo
        return self.total


class ItemVenda(models.Model):
    """
    Modelo para itens de venda.
    """
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', verbose_name=_('venda'))
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_venda', verbose_name=_('produto'))
    quantidade = models.DecimalField(_('quantidade'), max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(_('preço unitário'), max_digits=10, decimal_places=2)
    desconto = models.DecimalField(_('desconto'), max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(_('subtotal'), max_digits=10, decimal_places=2)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('item de venda')
        verbose_name_plural = _('itens de venda')
        ordering = ['id']

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para calcular o subtotal.
        """
        self.subtotal = (self.quantidade * self.preco_unitario) - self.desconto
        super().save(*args, **kwargs)


class FormaPagamento(models.Model):
    """
    Modelo para formas de pagamento.
    """
    TIPO_CHOICES = (
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('boleto', 'Boleto'),
        ('transferencia', 'Transferência'),
        ('cheque', 'Cheque'),
        ('crediario', 'Crediário'),
    )
    
    nome = models.CharField(_('nome'), max_length=100)
    tipo = models.CharField(_('tipo'), max_length=20, choices=TIPO_CHOICES)
    ativo = models.BooleanField(_('ativo'), default=True)
    taxa = models.DecimalField(_('taxa (%)'), max_digits=5, decimal_places=2, default=0)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('forma de pagamento')
        verbose_name_plural = _('formas de pagamento')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Pagamento(models.Model):
    """
    Modelo para pagamentos de vendas.
    """
    STATUS_CHOICES = (
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('recusado', 'Recusado'),
        ('cancelado', 'Cancelado'),
    )
    
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos', verbose_name=_('venda'))
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, related_name='pagamentos', verbose_name=_('forma de pagamento'))
    valor = models.DecimalField(_('valor'), max_digits=10, decimal_places=2)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_pagamento = models.DateTimeField(_('data do pagamento'), auto_now_add=True)
    
    # Campos adicionais para diferentes formas de pagamento
    parcelas = models.PositiveIntegerField(_('parcelas'), default=1)
    autorizacao = models.CharField(_('autorização'), max_length=50, blank=True, null=True)
    bandeira = models.CharField(_('bandeira'), max_length=50, blank=True, null=True)
    nsu = models.CharField(_('NSU'), max_length=50, blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('pagamento')
        verbose_name_plural = _('pagamentos')
        ordering = ['-data_pagamento']

    def __str__(self):
        return f"{self.forma_pagamento.nome} - R$ {self.valor}"
