from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsAdminOrReadOnly

# Placeholder para futura implementação
class NFEViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de notas fiscais eletrônicas.
    """
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def list(self, request):
        return Response({"message": "Lista de notas fiscais"}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        return Response({"message": f"Detalhes da nota fiscal {pk}"}, status=status.HTTP_200_OK)
    
    def create(self, request):
        return Response({"message": "Nota fiscal criada"}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        return Response({"message": f"Nota fiscal {pk} atualizada"}, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        return Response({"message": f"Nota fiscal {pk} excluída"}, status=status.HTTP_204_NO_CONTENT)
