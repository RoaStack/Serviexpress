from django.shortcuts import render, get_object_or_404
from .models import Boleta

def detalle_boleta(request, pk):
    """
    Muestra el detalle de una boleta, incluyendo cliente, servicios y repuestos asociados.
    """
    boleta = get_object_or_404(Boleta, pk=pk)

    # Calcular totales
    total_servicios = sum(s.precio_servicio for s in boleta.detalles_servicios.all())
    total_repuestos = sum(r.subtotal() for r in boleta.detalles_repuestos.all())
    total_general = total_servicios + total_repuestos

    contexto = {
        "boleta": boleta,
        "total_servicios": total_servicios,
        "total_repuestos": total_repuestos,
        "total_general": total_general,
    }

    return render(request, "boletas/detalle_boleta.html", contexto)

