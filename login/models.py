from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):

    TIPOS_USUARIO = [
        ('administrador', 'Administrador'),
        ('cliente', 'Cliente'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    def __str__(self):
        return f'{self.usuario.username} - {self.tipo_usuario}'
