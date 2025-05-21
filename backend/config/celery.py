import os
from celery import Celery

# Definir variáveis de ambiente para configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Criar instância do Celery
app = Celery('terman_os')

# Carregar configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobrir tarefas automaticamente
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
