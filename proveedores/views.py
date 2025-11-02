from django.shortcuts import render

# Create your views here.
def crear_proveedor(request):
    # Aquí iría la lógica para crear un proveedor
    return render(request, 'proveedores/crear_proveedor.html')