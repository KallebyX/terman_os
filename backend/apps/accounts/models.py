from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo User.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Modelo de usuário personalizado que usa email como identificador único.
    """
    username = None
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Nome', max_length=30)
    last_name = models.CharField('Sobrenome', max_length=150)
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_admin = models.BooleanField('Administrador', default=False)
    is_seller = models.BooleanField('Vendedor', default=False)
    is_operator = models.BooleanField('Operador', default=False)
    date_joined = models.DateTimeField('Data de cadastro', default=timezone.now)
    is_email_verified = models.BooleanField('Email verificado', default=False)
    password_reset_token = models.CharField('Token de redefinição de senha', max_length=100, null=True, blank=True)
    password_reset_expires = models.DateTimeField('Expiração do token', null=True, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_full_name(self):
        """
        Retorna o nome completo do usuário.
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """
        Retorna o primeiro nome do usuário.
        """
        return self.first_name
        
    @property
    def is_customer(self):
        """
        Verifica se o usuário é um cliente (não é admin, vendedor ou operador).
        """
        return not (self.is_admin or self.is_seller or self.is_operator)


class Profile(models.Model):
    """
    Modelo de perfil de usuário com informações adicionais.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('Telefone', max_length=20, blank=True, null=True)
    address = models.CharField('Endereço', max_length=255, blank=True, null=True)
    city = models.CharField('Cidade', max_length=100, blank=True, null=True)
    state = models.CharField('Estado', max_length=2, blank=True, null=True)
    zip_code = models.CharField('CEP', max_length=10, blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
