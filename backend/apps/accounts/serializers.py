from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Profile.
    """
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'city', 'state', 'zip_code']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User.
    """
    password = serializers.CharField(write_only=True, required=False)
    password_confirmation = serializers.CharField(write_only=True, required=False)
    profile = ProfileSerializer(required=False)
    user_type = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_admin', 'is_seller', 'is_operator',
                  'is_active', 'date_joined', 'last_login', 'is_email_verified',
                  'password', 'password_confirmation', 'profile', 'user_type']
        read_only_fields = ['id', 'date_joined', 'last_login', 'is_email_verified']
    
    def get_user_type(self, obj):
        """
        Retorna o tipo de usuário com base nas flags booleanas.
        """
        if obj.is_admin:
            return 'admin'
        elif obj.is_seller:
            return 'seller'
        elif obj.is_operator:
            return 'operator'
        else:
            return 'customer'
    
    def validate(self, attrs):
        # Validação de senha apenas quando criando um novo usuário ou atualizando senha
        if 'password' in attrs:
            password = attrs.get('password')
            password_confirmation = attrs.pop('password_confirmation', None)
            
            if not password_confirmation:
                raise serializers.ValidationError({"password_confirmation": "Confirmação de senha é obrigatória."})
            
            if password != password_confirmation:
                raise serializers.ValidationError({"password_confirmation": "As senhas não conferem."})
            
            validate_password(password)
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', None)
        
        # Atualizar campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Atualizar ou criar perfil
        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserCreateSerializer(UserSerializer):
    """
    Serializer para criação de usuários com validação de senha obrigatória.
    """
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer para login de usuários.
    """
    email = serializers.EmailField(required=True, error_messages={'required': 'O email é obrigatório.'})
    password = serializers.CharField(required=True, write_only=True, error_messages={'required': 'A senha é obrigatória.'})


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitação de redefinição de senha.
    """
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer para confirmação de redefinição de senha.
    """
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        
        if password != password_confirmation:
            raise serializers.ValidationError({"password_confirmation": "As senhas não conferem."})
        
        validate_password(password)
        return attrs
