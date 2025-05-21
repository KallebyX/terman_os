"""
URL Configuration for Terman OS project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.dashboard.views import HomeView

# API Schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Terman OS API",
        default_version='v1',
        description="API para o sistema Terman OS",
        terms_of_service="https://www.mangueirasterman.com.br/terms/",
        contact=openapi.Contact(email="contato@mangueirasterman.com.br"),
        license=openapi.License(name="Uso Restrito"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API endpoints
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/pos/', include('apps.pos.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/service-orders/', include('apps.service_orders.urls')),
    path('api/financial/', include('apps.financial.urls')),
    path('api/fiscal/', include('apps.fiscal.urls')),
    path('api/hr/', include('apps.hr.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('', HomeView.as_view(), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
