"""
Worker para tarefas em background - Terman OS

Este worker executa tarefas em background como:
- Processamento de relatórios
- Envio de emails em massa
- Sincronização de dados
- Limpeza de cache
"""
import os
import time
import signal
import sys
from datetime import datetime

from app import create_app, db

# Configuração do app Flask para contexto
app = create_app()

# Flag para controle de shutdown gracioso
running = True


def signal_handler(signum, frame):
    """Handler para shutdown gracioso"""
    global running
    print(f"[{datetime.now()}] Recebido sinal de shutdown. Finalizando...")
    running = False


def run_scheduled_tasks():
    """Executa tarefas agendadas"""
    with app.app_context():
        print(f"[{datetime.now()}] Executando verificação de tarefas...")
        # Placeholder para tarefas futuras:
        # - Verificar pedidos pendentes
        # - Processar filas de email
        # - Atualizar cache de produtos
        # - Sincronizar estoque


def main():
    """Loop principal do worker"""
    global running

    # Registra handlers de sinal
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    print(f"[{datetime.now()}] Worker Terman OS iniciado")
    print(f"[{datetime.now()}] Ambiente: {os.environ.get('FLASK_ENV', 'development')}")

    # Loop principal
    while running:
        try:
            run_scheduled_tasks()
            # Intervalo entre execuções (60 segundos)
            for _ in range(60):
                if not running:
                    break
                time.sleep(1)
        except Exception as e:
            print(f"[{datetime.now()}] Erro no worker: {e}")
            time.sleep(5)

    print(f"[{datetime.now()}] Worker finalizado com sucesso")
    sys.exit(0)


if __name__ == '__main__':
    main()
