from django.contrib import admin
from .models import Estoque, MovimentacaoEstoque


@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Estoque.
    """
    list_display = ('produto', 'quantidade_atual', 'quantidade_reservada', 'quantidade_disponivel', 'status', 'ultima_atualizacao')
    list_filter = ('produto__categorias',)
    search_fields = ('produto__nome', 'produto__codigo')
    readonly_fields = ('quantidade_disponivel', 'ultima_atualizacao')
    date_hierarchy = 'ultima_atualizacao'


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    """
    Admin para o modelo MovimentacaoEstoque.
    """
    list_display = ('produto', 'tipo', 'origem', 'quantidade', 'valor_unitario', 'usuario', 'data_movimentacao')
    list_filter = ('tipo', 'origem', 'data_movimentacao')
    search_fields = ('produto__nome', 'produto__codigo', 'documento', 'observacao')
    readonly_fields = ('data_movimentacao',)
    date_hierarchy = 'data_movimentacao'
    fieldsets = (
        (None, {
            'fields': ('produto', 'tipo', 'origem', 'quantidade', 'valor_unitario')
        }),
        ('Detalhes', {
            'fields': ('documento', 'observacao', 'usuario')
        }),
        ('Referência', {
            'fields': ('referencia_id', 'referencia_tipo'),
            'classes': ('collapse',)
        }),
    )
