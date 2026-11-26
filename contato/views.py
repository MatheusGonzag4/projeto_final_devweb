from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import FormContato
from .models import Contato


# qualquer visitante pode mandar mensagem, não precisa estar logado
def add_contato(request):
    form = FormContato(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Mensagem enviada! Em breve entraremos em contato.")
        return redirect("add_contato")

    return render(request, "add-contato.html", {"form": form})


@login_required
def contatos(request):
    return render(request, "contatos.html", {"contatos": Contato.objects.order_by("-id")})


@login_required
@require_POST
def del_contato(request, id_contato):
    contato = get_object_or_404(Contato, id=id_contato)
    contato.delete()
    messages.success(request, "Contato excluído.")
    return redirect("contatos")
