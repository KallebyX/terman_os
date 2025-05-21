from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
import uuid
import datetime

from .serializers import (
    UserSerializer, 
    UserCreateSerializer, 
    UserLoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .permissions import IsAdminOrSelf, IsAdminOrReadOnly

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de usuários.
    Administradores podem ver e editar todos os usuários.
    Usuários comuns podem apenas ver e editar seus próprios dados.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class UserRegistrationView(generics.CreateAPIView):
    """
    View para registro de novos usuários.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Gerar token de verificação de email
        token = str(uuid.uuid4())
        user.is_active = True  # Ativar usuário imediatamente, mas email não verificado
        user.save()
        
        # Enviar email de verificação (em produção)
        if not settings.DEBUG:
            try:
                context = {
                    'user': user,
                    'verification_url': f"{settings.FRONTEND_URL}/verify-email/{token}"
                }
                email_html = render_to_string('accounts/email_verification.html', context)
                email_text = render_to_string('accounts/email_verification.txt', context)
                
                send_mail(
                    subject='Verifique seu email - Mangueiras Terman',
                    message=email_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=email_html,
                    fail_silently=False,
                )
            except Exception as e:
                # Log do erro, mas não falha o registro
                print(f"Erro ao enviar email: {str(e)}")
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    """
    View para login de usuários.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'detail': 'Conta desativada.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Atualizar último login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        # Adicionar claims personalizados ao token
        refresh['user_id'] = user.id
        refresh['email'] = user.email
        refresh['is_admin'] = user.is_admin
        refresh['is_seller'] = user.is_seller
        refresh['is_operator'] = user.is_operator
        refresh['name'] = user.get_full_name()
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


class UserProfileView(APIView):
    """
    View para visualizar e atualizar o perfil do usuário logado.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PasswordResetRequestView(APIView):
    """
    View para solicitar redefinição de senha.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Gerar token e definir expiração
            token = get_random_string(64)
            user.password_reset_token = token
            user.password_reset_expires = timezone.now() + datetime.timedelta(hours=24)
            user.save(update_fields=['password_reset_token', 'password_reset_expires'])
            
            # Enviar email (em produção)
            if not settings.DEBUG:
                try:
                    context = {
                        'user': user,
                        'reset_url': f"{settings.FRONTEND_URL}/reset-password/{token}"
                    }
                    email_html = render_to_string('accounts/password_reset.html', context)
                    email_text = render_to_string('accounts/password_reset.txt', context)
                    
                    send_mail(
                        subject='Redefinição de senha - Mangueiras Terman',
                        message=email_text,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        html_message=email_html,
                        fail_silently=False,
                    )
                except Exception as e:
                    # Log do erro, mas não falha a solicitação
                    print(f"Erro ao enviar email: {str(e)}")
            
        except User.DoesNotExist:
            # Não informamos ao usuário se o email existe ou não por segurança
            pass
        
        return Response({'detail': 'Se o email estiver cadastrado, você receberá instruções para redefinir sua senha.'})


class PasswordResetConfirmView(APIView):
    """
    View para confirmar redefinição de senha.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(
                password_reset_token=token,
                password_reset_expires__gt=timezone.now()
            )
            
            # Definir nova senha
            user.set_password(password)
            user.password_reset_token = None
            user.password_reset_expires = None
            user.save()
            
            return Response({'detail': 'Senha redefinida com sucesso.'})
            
        except User.DoesNotExist:
            return Response({'detail': 'Token inválido ou expirado.'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    View para verificar email.
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, token):
        try:
            # Em uma implementação real, o token seria armazenado no banco de dados
            # e associado ao usuário. Aqui estamos simulando para fins de demonstração.
            user = User.objects.get(id=1)  # Simulação
            user.is_email_verified = True
            user.save(update_fields=['is_email_verified'])
            
            return Response({'detail': 'Email verificado com sucesso.'})
            
        except User.DoesNotExist:
            return Response({'detail': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Backend do Terman OS está rodando 🚀"})
