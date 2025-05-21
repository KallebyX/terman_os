from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSelf(BasePermission):
    """
    Permissão personalizada para permitir que administradores acessem qualquer usuário,
    mas usuários comuns só possam acessar seus próprios dados.
    """
    
    def has_permission(self, request, view):
        # Permitir acesso a administradores
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin):
            return True
        
        # Para outros usuários, permitir apenas acesso ao próprio perfil
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permitir acesso a administradores
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_admin):
            return True
        
        # Permitir acesso ao próprio usuário
        return obj.id == request.user.id


class IsAdminOrReadOnly(BasePermission):
    """
    Permissão personalizada para permitir que administradores tenham acesso total,
    mas outros usuários tenham apenas acesso de leitura.
    """
    
    def has_permission(self, request, view):
        # Permitir acesso de leitura para todos
        if request.method in SAFE_METHODS:
            return True
        
        # Permitir acesso de escrita apenas para administradores
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)
    
    def has_object_permission(self, request, view, obj):
        # Permitir acesso de leitura para todos
        if request.method in SAFE_METHODS:
            return True
        
        # Permitir acesso de escrita apenas para administradores
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_admin)


class IsSellerOrAdmin(BasePermission):
    """
    Permissão personalizada para permitir que vendedores e administradores tenham acesso.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_admin or request.user.is_seller or request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_admin or request.user.is_seller or request.user.is_staff


class IsOperatorOrAdmin(BasePermission):
    """
    Permissão personalizada para permitir que operadores e administradores tenham acesso.
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_admin or request.user.is_operator or request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        return request.user.is_admin or request.user.is_operator or request.user.is_staff
