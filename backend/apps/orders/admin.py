from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'total', 'payment_method')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('id', 'customer__email', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('subtotal', 'total', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('customer', 'status', 'created_at', 'updated_at')
        }),
        ('Pagamento', {
            'fields': ('payment_method', 'payment_date')
        }),
        ('Entrega', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip',
                      'shipping_date', 'delivery_date', 'tracking_code')
        }),
        ('Valores', {
            'fields': ('subtotal', 'discount', 'shipping_cost', 'total')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Impedir exclusão de pedidos que não estejam pendentes ou cancelados
        if obj and obj.status not in ['pending', 'canceled']:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__nome')
    readonly_fields = ('subtotal',)
    
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'Subtotal'
