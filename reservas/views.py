from django.shortcuts import render

# Create your views here.
def crear_reserva(request):
    # Aquí iría la lógica para crear una reserva
    return render(request, 'reservas/crear_reserva.html')