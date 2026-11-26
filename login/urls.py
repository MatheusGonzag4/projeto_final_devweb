from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", views.AlterarSenhaView.as_view(), name="alterar_senha"),

    # recuperação de senha: usa as views e as telas nativas do Django
    path("esqueci-senha/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("esqueci-senha/enviado/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("redefinir/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("redefinir/concluido/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
