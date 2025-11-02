from django.shortcuts import render

# Create your views here
def detalle_boleta(request, pk):
    # Aquí iría la lógica para obtener los detalles de la boleta desde la base de datos
    boleta = {}  # Reemplazar con la consulta real a la base de datos
    return render(request, 'boletas/detalle_boleta.html', {'boleta': boleta})