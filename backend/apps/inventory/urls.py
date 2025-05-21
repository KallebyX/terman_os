from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'inventory'

router = DefaultRouter()
router.register('estoque', views.EstoqueViewSet, basename='estoque')
router.register('movimentacoes', views.MovimentacaoEstoqueViewSet, basename='movimentacoes')

urlpatterns = [
    # Endpoints adicionais
    path('ajuste-estoque/', views.AjusteEstoqueView.as_view(), name='ajuste-estoque'),
    path('produtos-baixo-estoque/', views.ProdutosBaixoEstoqueView.as_view(), name='produtos-baixo-estoque'),
    path('relatorio-movimentacoes/', views.RelatorioMovimentacoesView.as_view(), name='relatorio-movimentacoes'),
]

urlpatterns += router.urls
