
# Importar o Celery para garantir que seja carregado quando o Django iniciar
from .celery import app as celery_app

__all__ = ('celery_app',)
