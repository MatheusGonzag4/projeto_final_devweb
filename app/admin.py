from django.contrib import admin
from .models import Categoria, Pedido, Servico

admin.site.register(Categoria)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ["nome", "descricao", "preco", "imagem", "categoria", "ativo"]
    list_filter = ["categoria", "ativo"]
    search_fields = ["nome", "descricao"]
    ordering = ["nome", "preco"]
    list_per_page = 25


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["usuario", "servico", "preco", "criado_em"]
    list_filter = ["criado_em"]
