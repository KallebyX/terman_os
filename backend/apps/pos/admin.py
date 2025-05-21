from django.contrib import admin
from .models import Cliente, Venda, ItemVenda, FormaPagamento, Pagamento


class ItemVendaInline(admin.TabularInline):
    """
    Inline para itens de venda no admin da venda.
    """
    model = ItemVenda
    extra = 1
    readonly_fields = ['subtotal']


class PagamentoInline(admin.TabularInline):
    """
    Inline para pagamentos no admin da venda.
    """
    model = Pagamento
    extra = 1
    readonly_fields = ['data_pagamento']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Cliente.
    """
    list_display = ('nome', 'tipo', 'documento', 'email', 'telefone', 'celular', 'cidade', 'ativo')
    list_filter = ('tipo', 'ativo', 'cidade', 'estado')
    search_fields = ('nome', 'razao_social', 'cpf', 'cnpj', 'email', 'telefone', 'celular')
    fieldsets = (
        (None, {
            'fields': ('tipo', 'nome', 'email', 'telefone', 'celular', 'ativo')
        }),
        ('Pessoa Física', {
            'fields': ('cpf', 'rg', 'data_nascimento'),
            'classes': ('collapse',)
        }),
        ('Pessoa Jurídica', {
            'fields': ('razao_social', 'cnpj', 'inscricao_estadual', 'inscricao_municipal', 'contato'),
            'classes': ('collapse',)
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')
        }),
        ('Financeiro', {
            'fields': ('limite_credito', 'observacoes')
        }),
        ('Usuário', {
            'fields': ('usuario',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Venda.
    """
    list_display = ('id', 'cliente', 'vendedor', 'data_venda', 'status', 'tipo', 'total', 'nfe_emitida')
    list_filter = ('status', 'tipo', 'data_venda', 'nfe_emitida')
    search_fields = ('cliente__nome', 'cliente__cpf', 'cliente__cnpj', 'observacoes')
    readonly_fields = ('data_venda', 'data_finalizacao', 'data_cancelamento')
    inlines = [ItemVendaInline, PagamentoInline]
    fieldsets = (
        (None, {
            'fields': ('cliente', 'vendedor', 'data_venda', 'status', 'tipo')
        }),
        ('Valores', {
            'fields': ('subtotal', 'desconto', 'acrescimo', 'total')
        }),
        ('Detalhes', {
            'fields': ('observacoes', 'data_finalizacao', 'data_cancelamento', 'motivo_cancelamento')
        }),
        ('Nota Fiscal', {
            'fields': ('nfe_emitida', 'nfe_numero', 'nfe_chave', 'nfe_data'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo FormaPagamento.
    """
    list_display = ('nome', 'tipo', 'ativo', 'taxa')
    list_filter = ('tipo', 'ativo')
    search_fields = ('nome',)
