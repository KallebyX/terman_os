"""
Utilitários para o projeto
"""
import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Manipulador de exceções personalizado para a API REST
    """
    # Primeiro, obtém a resposta padrão
    response = exception_handler(exc, context)

    # Se não houver resposta, é uma exceção não tratada
    if response is None:
        logger.error(f"Exceção não tratada: {exc}")
        logger.error(traceback.format_exc())
        
        # Retorna uma resposta de erro genérica
        return Response(
            {
                'detail': 'Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde.',
                'error': str(exc)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Adiciona mais informações à resposta
    if hasattr(exc, 'detail'):
        response.data = {
            'detail': exc.detail,
            'code': getattr(exc, 'code', 'error')
        }

    return response
