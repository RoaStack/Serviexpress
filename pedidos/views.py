from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import OrdenPedidoForm
from .models import DetalleOrden, OrdenPedido
from repuestos.models import Repuesto
import json
from usuarios.utils import es_mecanico



@login_required
@user_passes_test(es_mecanico)
def lista_ordenes(request):
    ordenes = OrdenPedido.objects.filter(mecanico=request.user.perfil).order_by('-fecha_creacion')

    return render(request, 'lista_ordenes.html', {
        'ordenes': ordenes
    })


@login_required
@user_passes_test(es_mecanico)
def crear_orden(request):
    repuestos = Repuesto.objects.all()

    if request.method == "POST":
        form = OrdenPedidoForm(request.POST)

        if form.is_valid():
            orden = form.save(commit=False)
            orden.mecanico = request.user.perfil
            orden.save()

            detalles = request.POST.get('detalles_json')
            detalles = json.loads(detalles)

            for det in detalles:
                DetalleOrden.objects.create(
                    orden=orden,
                    repuesto_id=det['repuesto_id'],
                    cantidad=det['cantidad'],
                    precio_unitario=det['precio_unitario'],
                )

            return redirect('pedidos:detalle_orden', orden_id=orden.id)
    else:
        form = OrdenPedidoForm()

    return render(request, 'crear_orden.html', {
        'form': form,
        'repuestos': repuestos,
    })

@login_required
@user_passes_test(es_mecanico)
def detalle_orden(request, orden_id):
    orden = get_object_or_404(OrdenPedido, id=orden_id, mecanico=request.user.perfil)

    detalles = orden.detalles.all()  

    return render(request, "detalle_orden.html", {
        "orden": orden,
        "detalles": detalles,
        "total": orden.monto_total,
    })

@login_required
@user_passes_test(es_mecanico)
# AJAX para obtener el precio de compra del repuesto
def obtener_precio_repuesto(request, repuesto_id):
    rep = Repuesto.objects.get(id=repuesto_id)
    return JsonResponse({'precio': rep.precio_compra})

@login_required
@user_passes_test(es_mecanico)
def recepcionar_orden(request, orden_id):
    orden = get_object_or_404(OrdenPedido, id=orden_id, mecanico=request.user.perfil)

    if request.method == "POST":
        for det in orden.detalles.all():
            cantidad_recibida = int(request.POST.get(f"cantidad_{det.id}", det.cantidad))

            # VALIDACIONES IMPORTANTES:
            if cantidad_recibida < 0:
                cantidad_recibida = 0   # no permitir negativos

            if cantidad_recibida > det.cantidad:
                cantidad_recibida = det.cantidad  # no permitir más de lo solicitado

            det.cantidad = cantidad_recibida
            det.save()

        orden.estado = "recibido"
        orden.save()

        return redirect("pedidos:detalle_orden", orden_id=orden.id)

    return render(request, "recepcionar_orden.html", {
        "orden": orden,
        "detalles": orden.detalles.all(),
        "total": orden.monto_total,
    })



