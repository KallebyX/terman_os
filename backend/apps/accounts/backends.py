"""
Backend de autenticação personalizado para autenticar usuários por email
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Autentica usando o email
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Tenta autenticar com email
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Retorna None se o usuário não existir
            return None
        except Exception as e:
            # Log de erro
            print(f"Erro no EmailBackend: {e}")
            return None
