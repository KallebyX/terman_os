from django.contrib import admin
from .models import Categoria, Produto, ImagemProduto, Fornecedor


class ImagemProdutoInline(admin.TabularInline):
    """
    Inline para imagens de produto no admin do produto.
    """
    model = ImagemProduto
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Categoria.
    """
    list_display = ('nome', 'slug', 'ativa', 'ordem')
    list_filter = ('ativa',)
    search_fields = ('nome', 'descricao')
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Produto.
    """
    list_display = ('codigo', 'nome', 'preco', 'preco_promocional', 'ativo', 'destaque')
    list_filter = ('ativo', 'destaque', 'categorias')
    search_fields = ('codigo', 'nome', 'descricao', 'codigo_barras')
    prepopulated_fields = {'slug': ('nome',)}
    filter_horizontal = ('categorias',)
    inlines = [ImagemProdutoInline]
    fieldsets = (
        (None, {
            'fields': ('codigo', 'nome', 'descricao', 'descricao_curta', 'categorias')
        }),
        ('Preços', {
            'fields': ('preco', 'preco_promocional')
        }),
        ('Dimensões e Especificações', {
            'fields': ('unidade', 'peso', 'altura', 'largura', 'comprimento')
        }),
        ('Estoque', {
            'fields': ('estoque_minimo', 'codigo_barras', 'ncm')
        }),
        ('Imagem', {
            'fields': ('imagem_principal',)
        }),
        ('Status', {
            'fields': ('ativo', 'destaque')
        }),
        ('SEO', {
            'fields': ('slug', 'meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Fornecedor.
    """
    list_display = ('nome', 'cnpj', 'telefone', 'email', 'ativo')
    list_filter = ('ativo', 'estado')
    search_fields = ('nome', 'razao_social', 'cnpj', 'email', 'contato')
    fieldsets = (
        (None, {
            'fields': ('nome', 'razao_social', 'cnpj', 'inscricao_estadual')
        }),
        ('Contato', {
            'fields': ('telefone', 'email', 'contato', 'site')
        }),
        ('Endereço', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
        }),
        ('Observações', {
            'fields': ('observacoes', 'ativo')
        }),
    )
