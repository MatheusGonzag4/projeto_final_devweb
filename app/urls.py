from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("quem-somos/", views.quemSomos, name="quemSomos"),
    path("produtos/", views.produtos, name="produtos"),

    path("servicos/", views.servicos, name="servicos"),
    path("add-servicos/", views.addServicos, name="addServicos"),
    path("edit-servicos/<int:id_servico>/", views.editServicos, name="editServicos"),
    path("del-servicos/<int:id_servico>/", views.delServicos, name="delServicos"),

    path("integrantes/", views.integrantes, name="integrantes"),
    path("add-integrante/", views.addIntegrante, name="addIntegrante"),
    path("edit-integrante/<int:id_integrante>/", views.editIntegrante, name="editIntegrante"),
    path("del-integrante/<int:id_integrante>/", views.delIntegrante, name="delIntegrante"),

    path("pedidos/", views.pedidos, name="pedidos"),
    path("comprar/<int:id_servico>/", views.comprar, name="comprar"),
    path("del-pedido/<int:id_pedido>/", views.delPedido, name="delPedido"),

    path("relatorios/", views.relatorios, name="relatorios"),

    path("categoria-api/", views.categoriasAPI, name="categoriasAPI"),
    path("categoria-api/<int:id_categoria>/", views.categoriaAPI, name="categoriaAPI"),
]
