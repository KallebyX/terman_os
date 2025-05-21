from django.db import models
from django.utils.translation import gettext_lazy as _


class Categoria(models.Model):
    """
    Modelo para categorias de produtos.
    """
    nome = models.CharField(_('nome'), max_length=100)
    descricao = models.TextField(_('descrição'), blank=True, null=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    imagem = models.ImageField(_('imagem'), upload_to='categorias/', blank=True, null=True)
    ativa = models.BooleanField(_('ativa'), default=True)
    ordem = models.PositiveIntegerField(_('ordem'), default=0)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('categoria')
        verbose_name_plural = _('categorias')
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Modelo para produtos.
    """
    UNIDADE_CHOICES = (
        ('un', 'Unidade'),
        ('m', 'Metro'),
        ('kg', 'Quilograma'),
        ('l', 'Litro'),
        ('pç', 'Peça'),
        ('cx', 'Caixa'),
        ('par', 'Par'),
    )
    
    codigo = models.CharField(_('código'), max_length=50, unique=True)
    nome = models.CharField(_('nome'), max_length=200)
    descricao = models.TextField(_('descrição'), blank=True, null=True)
    descricao_curta = models.CharField(_('descrição curta'), max_length=255, blank=True, null=True)
    preco = models.DecimalField(_('preço'), max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(_('preço promocional'), max_digits=10, decimal_places=2, blank=True, null=True)
    unidade = models.CharField(_('unidade'), max_length=10, choices=UNIDADE_CHOICES, default='un')
    peso = models.DecimalField(_('peso (kg)'), max_digits=10, decimal_places=3, blank=True, null=True)
    altura = models.DecimalField(_('altura (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    largura = models.DecimalField(_('largura (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    comprimento = models.DecimalField(_('comprimento (cm)'), max_digits=10, decimal_places=2, blank=True, null=True)
    imagem_principal = models.ImageField(_('imagem principal'), upload_to='produtos/', blank=True, null=True)
    categorias = models.ManyToManyField(Categoria, related_name='produtos', verbose_name=_('categorias'))
    ativo = models.BooleanField(_('ativo'), default=True)
    destaque = models.BooleanField(_('destaque'), default=False)
    estoque_minimo = models.DecimalField(_('estoque mínimo'), max_digits=10, decimal_places=2, default=0)
    codigo_barras = models.CharField(_('código de barras'), max_length=50, blank=True, null=True)
    ncm = models.CharField(_('NCM'), max_length=8, blank=True, null=True, help_text=_('Nomenclatura Comum do Mercosul'))
    
    # Campos para marketplace
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    meta_title = models.CharField(_('meta título'), max_length=100, blank=True, null=True)
    meta_description = models.CharField(_('meta descrição'), max_length=160, blank=True, null=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('produto')
        verbose_name_plural = _('produtos')
        ordering = ['nome']

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def verificar_estoque(self, quantidade):
        """
        Verifica se há estoque suficiente para a quantidade solicitada.
        """
        return self.estoque_minimo >= quantidade

    def atualizar_estoque(self, quantidade):
        """
        Atualiza o estoque do produto após uma venda.
        """
        if self.verificar_estoque(quantidade):
            self.estoque_minimo -= quantidade
            self.save()
        else:
            raise ValueError("Estoque insuficiente para a quantidade solicitada.")
    
    @property
    def preco_atual(self):
        """
        Retorna o preço atual do produto (promocional se disponível, senão o preço normal).
        """
        if self.preco_promocional:
            return self.preco_promocional
        return self.preco
    
    @property
    def tem_promocao(self):
        """
        Verifica se o produto está em promoção.
        """
        return self.preco_promocional is not None and self.preco_promocional < self.preco


class ImagemProduto(models.Model):
    """
    Modelo para imagens adicionais de produtos.
    """
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens', verbose_name=_('produto'))
    imagem = models.ImageField(_('imagem'), upload_to='produtos/')
    titulo = models.CharField(_('título'), max_length=100, blank=True, null=True)
    ordem = models.PositiveIntegerField(_('ordem'), default=0)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('imagem do produto')
        verbose_name_plural = _('imagens do produto')
        ordering = ['ordem']

    def __str__(self):
        return f"Imagem {self.ordem} - {self.produto.nome}"


class Fornecedor(models.Model):
    """
    Modelo para fornecedores de produtos.
    """
    nome = models.CharField(_('nome'), max_length=200)
    razao_social = models.CharField(_('razão social'), max_length=200, blank=True, null=True)
    cnpj = models.CharField(_('CNPJ'), max_length=18, blank=True, null=True)
    inscricao_estadual = models.CharField(_('inscrição estadual'), max_length=20, blank=True, null=True)
    endereco = models.CharField(_('endereço'), max_length=255, blank=True, null=True)
    cidade = models.CharField(_('cidade'), max_length=100, blank=True, null=True)
    estado = models.CharField(_('estado'), max_length=2, blank=True, null=True)
    cep = models.CharField(_('CEP'), max_length=10, blank=True, null=True)
    telefone = models.CharField(_('telefone'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    contato = models.CharField(_('contato'), max_length=100, blank=True, null=True)
    site = models.URLField(_('site'), blank=True, null=True)
    observacoes = models.TextField(_('observações'), blank=True, null=True)
    ativo = models.BooleanField(_('ativo'), default=True)
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('fornecedor')
        verbose_name_plural = _('fornecedores')
        ordering = ['nome']

    def __str__(self):
        return self.nome
