from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'products'

router = DefaultRouter()
router.register('categorias', views.CategoriaViewSet, basename='categorias')
router.register('produtos', views.ProdutoViewSet, basename='produtos')
router.register('fornecedores', views.FornecedorViewSet, basename='fornecedores')

urlpatterns = [
    # Endpoints adicionais
    path('produtos/destaque/', views.ProdutosDestaqueView.as_view(), name='produtos-destaque'),
    path('produtos/categoria/<slug:slug>/', views.ProdutosPorCategoriaView.as_view(), name='produtos-por-categoria'),
    path('produtos/<slug:slug>/', views.ProdutoDetailBySlugView.as_view(), name='produto-detail-by-slug'),
]

urlpatterns += router.urls
