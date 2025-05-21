from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# Removendo sinais relacionados ao Profile para permitir inicialização do backend
# Esses sinais podem ser restaurados após a criação do modelo Profile, se necessário
