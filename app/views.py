from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Min, ProtectedError, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

import logging
import os
import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import FormServico
from .models import Categoria, Pedido, Servico
from .serializers import CategoriaSerializer
from .supabase_client import get_supabase

logger = logging.getLogger(__name__)
AVISO_SUPABASE = "Não foi possível acessar o banco de dados remoto (Supabase). Tente novamente em instantes."


def carregar_produtos_parceiros(busca=""):
    """Busca produtos da API parceira sem derrubar a página quando ela falhar."""
    url = os.getenv("PARTNER_API_URL", "https://fakestoreapi.com/products").strip()
    try:
        timeout = max(5, int(os.getenv("PARTNER_API_TIMEOUT", "15")))
    except ValueError:
        timeout = 15

    try:
        resposta = requests.get(url, timeout=timeout)
        resposta.raise_for_status()
        produtos = resposta.json()
        if not isinstance(produtos, list):
            raise ValueError("A API parceira não retornou uma lista de produtos.")
        if busca:
            termo = busca.lower()
            produtos = [p for p in produtos if termo in p.get("title", "").lower()]
        return produtos, False
    except (requests.RequestException, ValueError, TypeError) as exc:
        logger.warning("Falha ao consumir API parceira %s: %s", url, exc)
        return [], True


# ---------- páginas públicas ----------

def index(request):
    destaques = Servico.objects.filter(ativo=True).select_related("categoria").order_by("-criado_em")[:4]
    categorias = Categoria.objects.filter(ativo=True)

    return render(request, "index.html", {"destaques": destaques, "categorias": categorias})


def quemSomos(request):
    integrantes = []

    try:
        resposta = get_supabase().table("integrantes").select("*").order("id").execute()
        integrantes = resposta.data
    except Exception:
        logger.exception("Falha ao consultar integrantes no Supabase")
        messages.error(request, AVISO_SUPABASE)

    return render(request, "quem-somos.html", {"integrantes": integrantes})


def produtos(request):
    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria", "")
    ordem = request.GET.get("ordem", "")

    produtos = Servico.objects.filter(ativo=True).select_related("categoria")

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria.isdigit():
        produtos = produtos.filter(categoria_id=categoria)

    if ordem == "menor":
        produtos = produtos.order_by("preco")
    elif ordem == "maior":
        produtos = produtos.order_by("-preco")
    else:
        produtos = produtos.order_by("nome")

    produtos_api = []
    api_fora = False

    # os produtos dos parceiros não têm categoria, então somem quando uma categoria é escolhida
    if not categoria:
        produtos_api, api_fora = carregar_produtos_parceiros(busca)

    return render(request, "produtos.html", {
        "produtos": produtos,
        "produtos_api": produtos_api,
        "api_fora": api_fora,
        "categorias": Categoria.objects.filter(ativo=True),
        "busca": busca,
        "categoria": categoria,
        "ordem": ordem,
        "filtrando": bool(busca or categoria or ordem),
    })


# ---------- pedidos ----------

@login_required
@require_POST
def comprar(request, id_servico):
    servico = get_object_or_404(Servico, id=id_servico, ativo=True)
    Pedido.objects.create(usuario=request.user, servico=servico, preco=servico.preco)

    messages.success(request, f"{servico.nome} foi adicionado aos seus pedidos.")
    return redirect("pedidos")


@login_required
def pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).select_related("servico")
    total = pedidos.aggregate(total=Sum("preco"))["total"] or 0

    return render(request, "pedidos.html", {"pedidos": pedidos, "total": total})


@login_required
@require_POST
def delPedido(request, id_pedido):
    pedido = get_object_or_404(Pedido, id=id_pedido, usuario=request.user)
    pedido.delete()

    messages.success(request, "Pedido removido.")
    return redirect("pedidos")


# ---------- serviços ----------

@login_required
def servicos(request):
    todos = Servico.objects.all()

    # os números do topo são do catálogo inteiro, não mudam com os filtros
    numeros = todos.aggregate(menor=Min("preco"), maior=Max("preco"))
    total_servicos = todos.count()
    ativos = todos.filter(ativo=True).count()

    servicos = todos.select_related("categoria")

    busca = request.GET.get("busca", "").strip()
    categoria = request.GET.get("categoria")
    preco = request.GET.get("preco")
    ordem = request.GET.get("ordem")

    if busca:
        servicos = servicos.filter(nome__icontains=busca)

    if categoria:
        servicos = servicos.filter(categoria_id=categoria)

    if preco == "baixo":
        servicos = servicos.filter(preco__lte=500)
    elif preco == "medio":
        servicos = servicos.filter(preco__gt=500, preco__lte=1500)
    elif preco == "alto":
        servicos = servicos.filter(preco__gt=1500)

    if ordem == "menor":
        servicos = servicos.order_by("preco")
    elif ordem == "maior":
        servicos = servicos.order_by("-preco")
    else:
        servicos = servicos.order_by("nome")

    contexto = {
        "servicos": servicos,
        "total_servicos": total_servicos,
        "ativos": ativos,
        "inativos": total_servicos - ativos,
        "mais_barato": numeros["menor"],
        "mais_caro": numeros["maior"],
        "categorias": Categoria.objects.filter(ativo=True),
        "busca": busca,
        "categoria": categoria,
        "preco": preco,
        "ordem": ordem,
        "filtrando": bool(busca or categoria or preco or ordem),
    }

    return render(request, "servicos.html", contexto)


@login_required
def addServicos(request):
    form = FormServico(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Serviço cadastrado.")
        return redirect("servicos")

    return render(request, "add-servicos.html", {"form": form})


@login_required
def editServicos(request, id_servico):
    servico = get_object_or_404(Servico, id=id_servico)
    form = FormServico(request.POST or None, request.FILES or None, instance=servico)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Serviço atualizado.")
        return redirect("servicos")

    return render(request, "edit-servicos.html", {"form": form, "servico": servico})


@login_required
@require_POST
def delServicos(request, id_servico):
    servico = get_object_or_404(Servico, id=id_servico)

    try:
        servico.delete()
        messages.success(request, "Serviço excluído.")
    except ProtectedError:
        messages.error(request, "Esse serviço já tem pedidos e não pode ser excluído. Desative-o em vez disso.")

    return redirect("servicos")


# ---------- equipe (dados no Supabase) ----------

@login_required
def integrantes(request):
    lista = []

    try:
        resposta = get_supabase().table("integrantes").select("*").order("id").execute()
        lista = resposta.data
    except Exception:
        logger.exception("Falha ao consultar integrantes no Supabase")
        messages.error(request, AVISO_SUPABASE)

    return render(request, "integrantes.html", {"integrantes": lista})


@login_required
def addIntegrante(request):
    if request.method == "POST":
        dados = {
            "nome": request.POST.get("nome", "").strip(),
            "cargo": request.POST.get("cargo", "").strip(),
            "biografia": request.POST.get("biografia", "").strip(),
            "foto_url": request.POST.get("foto", "").strip(),
        }

        try:
            get_supabase().table("integrantes").insert(dados).execute()
            messages.success(request, "Integrante cadastrado.")
            return redirect("integrantes")
        except Exception:
            logger.exception("Falha ao inserir integrante no Supabase")
            messages.error(request, AVISO_SUPABASE)
            return render(request, "add-integrante.html", {"dados": dados})

    return render(request, "add-integrante.html")


@login_required
def editIntegrante(request, id_integrante):
    if request.method == "POST":
        dados = {
            "nome": request.POST.get("nome", "").strip(),
            "cargo": request.POST.get("cargo", "").strip(),
            "biografia": request.POST.get("biografia", "").strip(),
            "foto_url": request.POST.get("foto", "").strip(),
        }

        try:
            get_supabase().table("integrantes").update(dados).eq("id", id_integrante).execute()
            messages.success(request, "Integrante atualizado.")
            return redirect("integrantes")
        except Exception:
            logger.exception("Falha ao atualizar integrante no Supabase")
            messages.error(request, AVISO_SUPABASE)
            dados["id"] = id_integrante
            return render(request, "edit-integrante.html", {"integrante": dados})

    try:
        resposta = get_supabase().table("integrantes").select("*").eq("id", id_integrante).execute()
    except Exception:
        logger.exception("Falha ao consultar integrante no Supabase")
        messages.error(request, AVISO_SUPABASE)
        return redirect("integrantes")

    if not resposta.data:
        messages.error(request, "Integrante não encontrado.")
        return redirect("integrantes")

    return render(request, "edit-integrante.html", {"integrante": resposta.data[0]})


@login_required
@require_POST
def delIntegrante(request, id_integrante):
    try:
        get_supabase().table("integrantes").delete().eq("id", id_integrante).execute()
        messages.success(request, "Integrante excluído.")
    except Exception:
        logger.exception("Falha ao excluir integrante no Supabase")
        messages.error(request, AVISO_SUPABASE)

    return redirect("integrantes")


# ---------- relatórios ----------

@login_required
def relatorios(request):
    servicos = Servico.objects.all()

    servicos_ativos = servicos.filter(ativo=True).count()
    servicos_inativos = servicos.filter(ativo=False).count()

    categorias = servicos.values("categoria__nome").annotate(quantidade=Count("id")).order_by("categoria__nome")

    return render(request, "relatorio.html", {
        "total_servicos": servicos.count(),
        "servicos_ativos": servicos_ativos,
        "servicos_inativos": servicos_inativos,
        "categorias_labels": [item["categoria__nome"] or "Sem categoria" for item in categorias],
        "categorias_valores": [item["quantidade"] for item in categorias],
    })


# ---------- API de categorias (Django REST Framework) ----------

@api_view(['GET', 'POST'])
def categoriasAPI(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    serializer = CategoriaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def categoriaAPI(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CategoriaSerializer(categoria, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
