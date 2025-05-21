from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir que apenas o proprietário do pedido
    ou administradores/vendedores possam acessá-lo.
    """
    
    def has_object_permission(self, request, view, obj):
        # Verificar se o usuário é o proprietário do pedido
        if hasattr(obj, 'customer'):
            return obj.customer == request.user or request.user.is_admin or request.user.is_seller
        
        # Para OrderItem, verificar o proprietário do pedido
        if hasattr(obj, 'order'):
            return obj.order.customer == request.user or request.user.is_admin or request.user.is_seller
        
        return False


class IsSellerOrAdmin(permissions.BasePermission):
    """
    Permissão personalizada para permitir acesso apenas a vendedores e administradores.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_seller)
