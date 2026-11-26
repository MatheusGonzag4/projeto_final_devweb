from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


# usuário criado pelo painel admin também ganha um perfil
@receiver(post_save, sender=User)
def criarPerfil(sender, instance, created, **kwargs):
    if created:
        tipo = 'administrador' if instance.is_superuser else 'cliente'
        Perfil.objects.get_or_create(usuario=instance, defaults={'tipo_usuario': tipo})
