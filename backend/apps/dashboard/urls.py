from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# Adicionar rotas quando as views forem implementadas
# router.register(r'dashboard', views.DashboardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
]
