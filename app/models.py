from django.conf import settings
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, default="Geral")
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='servicos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='servicos', null=True, blank=True)

    class Meta:
        verbose_name = 'serviço'
        verbose_name_plural = 'serviços'

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='pedidos')
    # guarda o preço da hora da compra, caso o serviço mude de valor depois
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.usuario.username} - {self.servico.nome}'
