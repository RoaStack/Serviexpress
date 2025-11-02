from django.shortcuts import render

# Create your views here.
def crear_pedido(request):
    # Aquí iría la lógica para crear un pedido
    return render(request, 'pedidos/crear_pedido.html')