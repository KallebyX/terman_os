from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsAdminOrReadOnly

class DashboardSummaryView(APIView):
    """
    View para fornecer resumo de dados para o dashboard.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Placeholder para implementação real
        # Em uma implementação completa, buscaria dados de vários modelos
        
        return Response({
            "sales_summary": {
                "today": 0,
                "week": 0,
                "month": 0,
                "year": 0
            },
            "inventory_summary": {
                "total_products": 0,
                "low_stock": 0,
                "out_of_stock": 0
            },
            "service_orders": {
                "pending": 0,
                "in_progress": 0,
                "completed": 0
            },
            "financial": {
                "receivables": 0,
                "payables": 0,
                "balance": 0
            }
        }, status=status.HTTP_200_OK)

from django.http import JsonResponse
from django.views import View

class HomeView(View):
    def get(self, request):
        return JsonResponse({"mensagem": "Bem-vindo ao Terman OS 🚀"})
