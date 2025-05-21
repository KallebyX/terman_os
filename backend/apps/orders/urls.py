from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='pedidos')

urlpatterns = [
    path('', include(router.urls)),
    path('my-orders/', views.MyOrdersView.as_view(), name='my-orders'),
]
