#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    
    # Verificar conexão com o banco de dados antes de executar comandos
    if len(sys.argv) > 1 and sys.argv[1] in ['runserver', 'migrate', 'makemigrations']:
        try:
            import django
            django.setup()
            from django.db import connection
            connection.ensure_connection()
            print("✅ Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")
            if 'migrate' not in sys.argv:
                print("⚠️ Continuando mesmo com erro de conexão...")
    
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
