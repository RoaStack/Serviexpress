from django.shortcuts import render

def servicio_list(request):
    # Aquí iría la lógica para obtener la lista de servicios desde la base de datos
    servicios = []  # Reemplazar con la consulta real a la base de datos
    return render(request, 'servicios/servicio_list.html', {'servicios': servicios})
