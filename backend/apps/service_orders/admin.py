from django.contrib import admin
from .models import OrdemServico, ItemOrdemServico, EtapaOrdemServico, ComentarioOrdemServico, AnexoOrdemServico


class ItemOrdemServicoInline(admin.TabularInline):
    """
    Inline para itens de ordem de serviço no admin da ordem de serviço.
    """
    model = ItemOrdemServico
    extra = 1
    readonly_fields = ['subtotal']


class EtapaOrdemServicoInline(admin.TabularInline):
    """
    Inline para etapas de ordem de serviço no admin da ordem de serviço.
    """
    model = EtapaOrdemServico
    extra = 1
    readonly_fields = ['data_inicio', 'data_conclusao']


class ComentarioOrdemServicoInline(admin.StackedInline):
    """
    Inline para comentários de ordem de serviço no admin da ordem de serviço.
    """
    model = ComentarioOrdemServico
    extra = 0
    readonly_fields = ['usuario', 'data']
    fields = ['usuario', 'data', 'texto']


class AnexoOrdemServicoInline(admin.TabularInline):
    """
    Inline para anexos de ordem de serviço no admin da ordem de serviço.
    """
    model = AnexoOrdemServico
    extra = 0
    readonly_fields = ['usuario', 'data']
    fields = ['usuario', 'data', 'arquivo', 'nome', 'descricao']


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo OrdemServico.
    """
    list_display = ('numero', 'cliente', 'responsavel', 'tecnico', 'data_abertura', 'status', 'prioridade', 'valor_total')
    list_filter = ('status', 'prioridade', 'data_abertura')
    search_fields = ('numero', 'cliente__nome', 'descricao_problema', 'descricao_servico')
    readonly_fields = ('numero', 'data_abertura', 'data_aprovacao', 'data_inicio', 'data_conclusao', 'data_cancelamento', 'valor_total')
    inlines = [ItemOrdemServicoInline, EtapaOrdemServicoInline, ComentarioOrdemServicoInline, AnexoOrdemServicoInline]
    fieldsets = (
        (None, {
            'fields': ('numero', 'cliente', 'responsavel', 'tecnico', 'data_abertura', 'status', 'prioridade')
        }),
        ('Datas', {
            'fields': ('data_aprovacao', 'data_inicio', 'data_conclusao', 'data_cancelamento'),
            'classes': ('collapse',)
        }),
        ('Descrições', {
            'fields': ('descricao_problema', 'descricao_servico', 'observacoes')
        }),
        ('Valores', {
            'fields': ('valor_servico', 'valor_pecas', 'valor_total', 'garantia')
        }),
        ('Cancelamento', {
            'fields': ('motivo_cancelamento',),
            'classes': ('collapse',)
        }),
    )


@admin.register(EtapaOrdemServico)
class EtapaOrdemServicoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo EtapaOrdemServico.
    """
    list_display = ('nome', 'ordem_servico', 'status', 'responsavel', 'ordem', 'data_inicio', 'data_conclusao')
    list_filter = ('status', 'data_inicio', 'data_conclusao')
    search_fields = ('nome', 'descricao', 'ordem_servico__numero')
    readonly_fields = ('data_inicio', 'data_conclusao')


@admin.register(ComentarioOrdemServico)
class ComentarioOrdemServicoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo ComentarioOrdemServico.
    """
    list_display = ('ordem_servico', 'usuario', 'data')
    list_filter = ('data',)
    search_fields = ('texto', 'ordem_servico__numero')
    readonly_fields = ('data',)


@admin.register(AnexoOrdemServico)
class AnexoOrdemServicoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo AnexoOrdemServico.
    """
    list_display = ('nome', 'ordem_servico', 'usuario', 'data')
    list_filter = ('data',)
    search_fields = ('nome', 'descricao', 'ordem_servico__numero')
    readonly_fields = ('data',)
