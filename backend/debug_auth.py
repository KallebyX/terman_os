"""
Script para depurar problemas de autenticação
"""
import os
import django
import sys
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model, authenticate
from django.db import connection

User = get_user_model()

def debug_auth(email, password):
    """
    Depura problemas de autenticação
    """
    print("\n===== DEPURAÇÃO DE AUTENTICAÇÃO =====")
    print(f"Tentando autenticar usuário: {email}")
    
    # Verifica se o usuário existe
    try:
        user = User.objects.get(email=email)
        print(f"✅ Usuário encontrado no banco de dados:")
        print(f"  - ID: {user.id}")
        print(f"  - Email: {user.email}")
        print(f"  - Nome: {user.first_name} {user.last_name}")
        print(f"  - Superusuário: {user.is_superuser}")
        print(f"  - Staff: {user.is_staff}")
        print(f"  - Admin: {user.is_admin}")
        print(f"  - Ativo: {user.is_active}")
        
        # Tenta autenticar
        auth_user = authenticate(email=email, password=password)
        if auth_user:
            print(f"✅ Autenticação bem-sucedida!")
            print(f"  - ID autenticado: {auth_user.id}")
            print(f"  - Email autenticado: {auth_user.email}")
        else:
            print(f"❌ Falha na autenticação!")
            print(f"  - Senha correta? {user.check_password(password)}")
            
            # Verifica se há um backend de autenticação configurado
            from django.conf import settings
            print(f"  - Backends de autenticação: {settings.AUTHENTICATION_BACKENDS}")
            
    except User.DoesNotExist:
        print(f"❌ Usuário com email {email} não encontrado no banco de dados!")
        
        # Lista todos os usuários
        all_users = User.objects.all()
        print(f"\nUsuários disponíveis no banco de dados ({all_users.count()}):")
        for u in all_users:
            print(f"  - {u.email} (ID: {u.id})")
    
    # Verifica a conexão com o banco de dados
    print("\n----- Informações do Banco de Dados -----")
    print(f"Conexão ativa: {connection.is_usable()}")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            print(f"Versão do PostgreSQL: {db_version}")
            
            # Verifica a tabela de usuários
            cursor.execute(f"SELECT COUNT(*) FROM {User._meta.db_table};")
            user_count = cursor.fetchone()[0]
            print(f"Total de usuários na tabela: {user_count}")
    except Exception as e:
        print(f"Erro ao consultar o banco de dados: {e}")
    
    print("\n===== FIM DA DEPURAÇÃO =====")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        email = input("Email: ")
        password = input("Senha: ")
    
    debug_auth(email, password)
