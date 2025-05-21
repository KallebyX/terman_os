from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'pos'

router = DefaultRouter()
router.register('clientes', views.ClienteViewSet, basename='clientes')
router.register('vendas', views.VendaViewSet, basename='vendas')
router.register('formas-pagamento', views.FormaPagamentoViewSet, basename='formas-pagamento')

urlpatterns = [
    # Endpoints adicionais
    path('vendas/<int:pk>/finalizar/', views.VendaFinalizarView.as_view(), name='venda-finalizar'),
    path('vendas/<int:pk>/cancelar/', views.VendaCancelarView.as_view(), name='venda-cancelar'),
    path('vendas/<int:venda_id>/itens/', views.ItemVendaListCreateView.as_view(), name='venda-itens'),
    path('vendas/<int:venda_id>/itens/<int:pk>/', views.ItemVendaDetailView.as_view(), name='venda-item-detail'),
    path('vendas/<int:venda_id>/pagamentos/', views.PagamentoListView.as_view(), name='venda-pagamentos'),
    path('relatorio-vendas/', views.RelatorioVendasView.as_view(), name='relatorio-vendas'),
    path('dashboard-vendas/', views.DashboardVendasView.as_view(), name='dashboard-vendas'),
]

urlpatterns += router.urls
