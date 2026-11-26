from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import CadastroForm, PerfilForm
from .models import Perfil


@login_required
def dashboard(request):
    # superusuários criados pelo terminal podem não ter perfil ainda
    tipo_padrao = 'administrador' if request.user.is_superuser else 'cliente'
    perfil, criado = Perfil.objects.get_or_create(usuario=request.user, defaults={'tipo_usuario': tipo_padrao})

    if perfil.tipo_usuario == 'administrador':
        return redirect("/admin/")

    return render(request, "dashboard.html")


@login_required
def perfil(request):
    form = PerfilForm(request.POST or None, instance=request.user)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Dados atualizados.")
        return redirect("perfil")

    return render(request, "perfil.html", {"form": form})


class AlterarSenhaView(SuccessMessageMixin, PasswordChangeView):
    template_name = "alterar_senha.html"
    success_url = reverse_lazy("perfil")
    success_message = "Senha alterada com sucesso."


def cadastro(request):
    form = CadastroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # o perfil de cliente é criado automaticamente (login/signals.py)
        form.save()
        messages.success(request, "Conta criada! Entre com seu usuário e senha.")
        return redirect('login')

    return render(request, 'cadastro.html', {'form': form})
