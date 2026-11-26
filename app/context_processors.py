from .models import Pedido


# número de pedidos que aparece na sacola do topo
def contador_pedidos(request):
    if request.user.is_authenticated:
        return {"qtd_pedidos": Pedido.objects.filter(usuario=request.user).count()}
    return {}
