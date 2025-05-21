from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin personalizado para o modelo User.
    """
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_seller', 'is_operator', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_admin', 'is_seller', 'is_operator', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name')}),
        (_('Tipo de Usuário'), {'fields': ('is_admin', 'is_seller', 'is_operator')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Profile.
    """
    list_display = ('user', 'phone', 'city', 'state')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone', 'city', 'state')
    raw_id_fields = ('user',)
