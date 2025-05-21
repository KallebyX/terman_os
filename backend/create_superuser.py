"""
Script para criar um superusuário
"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

def create_superuser(email, password, first_name="Admin", last_name="User"):
    """
    Cria um superusuário com os dados fornecidos
    """
    try:
        with transaction.atomic():
            # Verifica se o usuário já existe
            try:
                user = User.objects.get(email=email)
                print(f"Usuário com email {email} já existe. Atualizando permissões...")
            except User.DoesNotExist:
                # Cria um novo usuário
                user = User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=True,
                )
                print(f"Criando novo usuário com email {email}...")
            
            # Define as permissões de administrador
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.set_password(password)
            user.save()
            
            # Verifica se o usuário foi salvo corretamente
            user_check = User.objects.get(email=email)
            if not user_check.check_password(password):
                print("⚠️ AVISO: A senha não foi definida corretamente!")
            else:
                print("✅ Senha definida corretamente.")
            
            print(f"✅ Superusuário {email} criado/atualizado com sucesso!")
            print(f"Detalhes do usuário:")
            print(f"  - Email: {user.email}")
            print(f"  - Nome: {user.first_name} {user.last_name}")
            print(f"  - Superusuário: {user.is_superuser}")
            print(f"  - Staff: {user.is_staff}")
            print(f"  - Admin: {user.is_admin}")
            print(f"  - Ativo: {user.is_active}")
            
            return user
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) > 2:
        email = sys.argv[1]
        password = sys.argv[2]
        first_name = sys.argv[3] if len(sys.argv) > 3 else "Admin"
        last_name = sys.argv[4] if len(sys.argv) > 4 else "User"
        create_superuser(email, password, first_name, last_name)
    else:
        email = "admin@example.com"
        password = "Admin@123"  # Senha mais segura
        create_superuser(email, password)
