from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.urls")),
    path('contato/', include("contato.urls")),
    path('login/', include("login.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Fallback para o caso de o comando de build do Render não executar collectstatic.
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.BASE_DIR / "app" / "static",
    insecure=True,
)
