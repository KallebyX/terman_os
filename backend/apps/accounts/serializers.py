from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo User.
    """
    password = serializers.CharField(write_only=True, required=False)
    password_confirmation = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_admin', 'is_seller', 'is_operator',
                  'is_active', 'date_joined', 'last_login',
                  'password', 'password_confirmation']
        read_only_fields = ['id', 'date_joined', 'last_login']
    
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
        
        # Atualizar campos do usuário
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
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
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


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
