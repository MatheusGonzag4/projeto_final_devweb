from django.urls import path
from . import views

urlpatterns = [
    path("", views.add_contato, name="add_contato"),
    path("contatos/", views.contatos, name="contatos"),
    path("del-contato/<int:id_contato>/", views.del_contato, name="del_contato"),
]
