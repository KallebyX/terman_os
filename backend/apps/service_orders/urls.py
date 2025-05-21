from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'service_orders'

router = DefaultRouter()
router.register('ordens', views.OrdemServicoViewSet, basename='ordens')
router.register('etapas', views.EtapaOrdemServicoViewSet, basename='etapas')

urlpatterns = [
    # Endpoints adicionais
    path('ordens/<int:ordem_id>/itens/', views.ItemOrdemServicoListCreateView.as_view(), name='ordem-itens'),
    path('ordens/<int:ordem_id>/itens/<int:pk>/', views.ItemOrdemServicoDetailView.as_view(), name='ordem-item-detail'),
    path('ordens/<int:ordem_id>/comentarios/', views.ComentarioOrdemServicoListCreateView.as_view(), name='ordem-comentarios'),
    path('ordens/<int:ordem_id>/anexos/', views.AnexoOrdemServicoListCreateView.as_view(), name='ordem-anexos'),
    path('ordens/<int:pk>/aprovar/', views.OrdemServicoAprovarView.as_view(), name='ordem-aprovar'),
    path('ordens/<int:pk>/iniciar/', views.OrdemServicoIniciarView.as_view(), name='ordem-iniciar'),
    path('ordens/<int:pk>/concluir/', views.OrdemServicoConcluirView.as_view(), name='ordem-concluir'),
    path('ordens/<int:pk>/cancelar/', views.OrdemServicoCancelarView.as_view(), name='ordem-cancelar'),
    path('painel-industrial/', views.PainelIndustrialView.as_view(), name='painel-industrial'),
    path('relatorio-ordens/', views.RelatorioOrdensServicoView.as_view(), name='relatorio-ordens'),
]

urlpatterns += router.urls
