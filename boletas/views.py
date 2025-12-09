from django.shortcuts import render, get_object_or_404
from .models import Boleta
from usuarios.utils import es_cliente, es_mecanico
def detalle_boleta(request, pk):
    boleta = get_object_or_404(Boleta, pk=pk)

    # Calcular totales
    total_servicios = sum(s.precio_servicio for s in boleta.detalles_servicios.all())
    total_repuestos = sum(r.subtotal() for r in boleta.detalles_repuestos.all())
    total_general = total_servicios + total_repuestos

    # 🔙 Ruta + texto del botón según rol
    if es_mecanico(request.user):
        # nombre de la URL en reservas/urls.py -> name="historial_servicios"
        volver_url  = "reservas:historial_servicios"
        volver_text = "← Volver al Historial"
        body_class  = "mecanico-body"
    elif es_cliente:
        # nombre de la URL en reservas/urls.py -> name="servicios_realizados_cliente"
        volver_url  = "reservas:servicios_realizados_cliente"
        volver_text = "← Volver a Servicios Realizados"
        body_class  = "cliente-body"
    else:
        # Fallback para otros roles raros
        volver_url  = "usuarios:dashboard"
        volver_text = "← Volver al Dashboard"
        body_class  = ""

    contexto = {
        "boleta": boleta,
        "total_servicios": total_servicios,
        "total_repuestos": total_repuestos,
        "total_general": total_general,
        "body_class": body_class,
        "volver_url": volver_url,
        "volver_text": volver_text,
    }

    return render(request, "boletas/detalle_boleta.html", contexto)





