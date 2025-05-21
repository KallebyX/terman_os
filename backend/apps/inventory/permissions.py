from rest_framework import permissions

class IsSellerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir acesso apenas a vendedores e administradores.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_admin or request.user.is_seller
