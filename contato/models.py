from django.db import models


class Contato(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True)
    mensagem = models.TextField()

    class Meta:
        # a tabela já existia (criada pelo app "app"), então o nome continua o mesmo
        db_table = "contato_contato"

    def __str__(self):
        return self.nome
