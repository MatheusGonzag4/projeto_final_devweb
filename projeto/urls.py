from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from pathlib import Path

from django.conf import settings
from django.conf.urls.static import static

DJANGO_ADMIN_STATIC_ROOT = Path(admin.__file__).resolve().parent / "static" / "admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('contato/', include("contato.urls")),
    path('login/', include("login.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Fallback para o caso de o comando de build do Render não executar collectstatic.
urlpatterns += [
    # Fallback para os estáticos internos do Django Admin quando o ambiente
    # de produção não disponibilizar a pasta coletada pelo WhiteNoise.
    path(
        "static/admin/<path:path>",
        serve,
        {"document_root": DJANGO_ADMIN_STATIC_ROOT},
    ),
    path(
        "assets/admin/<path:path>",
        serve,
        {"document_root": DJANGO_ADMIN_STATIC_ROOT},
    ),
    path(
        "static/<path:path>",
        serve,
        {"document_root": settings.BASE_DIR / "app" / "static"},
    ),
    path(
        "assets/<path:path>",
        serve,
        {"document_root": settings.BASE_DIR / "app" / "static"},
    ),
]
