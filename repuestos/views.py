from django.shortcuts import render

# Create your views here.
def crear_repuesto(request):
    # Aquí iría la lógica para crear un repuesto
    return render(request, 'repuestos/crear_repuesto.html')