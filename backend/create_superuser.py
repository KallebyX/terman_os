"""
Script para criar um superusuário
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(email, password, first_name="Admin", last_name="User"):
    """
    Cria um superusuário com os dados fornecidos
    """
    try:
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
        
        print(f"✅ Superusuário {email} criado/atualizado com sucesso!")
        return user
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {e}")
        return None

if __name__ == "__main__":
    email = "admin@example.com"
    password = "admin123"
    create_superuser(email, password)
