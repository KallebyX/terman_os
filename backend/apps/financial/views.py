from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Placeholder para futura implementação
class TransactionViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de transações financeiras.
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        return Response({"message": "Lista de transações financeiras"}, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        return Response({"message": f"Detalhes da transação {pk}"}, status=status.HTTP_200_OK)
    
    def create(self, request):
        return Response({"message": "Transação criada"}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        return Response({"message": f"Transação {pk} atualizada"}, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        return Response({"message": f"Transação {pk} excluída"}, status=status.HTTP_204_NO_CONTENT)
