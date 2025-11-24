<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import OrdenPedidoForm
from .models import DetalleOrden, OrdenPedido
=======
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import OrdenPedidoForm
from .models import DetalleOrden
>>>>>>> staging
from repuestos.models import Repuesto
import json


def es_mecanico(user):
    return user.is_authenticated and user.groups.filter(name='Mecanicos').exists()

<<<<<<< HEAD
@login_required
@user_passes_test(es_mecanico)
def lista_ordenes(request):
    ordenes = OrdenPedido.objects.filter(mecanico=request.user.perfil).order_by('-fecha_creacion')

    return render(request, 'lista_ordenes.html', {
        'ordenes': ordenes
    })

=======
>>>>>>> staging

@login_required
@user_passes_test(es_mecanico)
def crear_orden(request):
<<<<<<< HEAD
=======
    form = OrdenPedidoForm()
>>>>>>> staging
    repuestos = Repuesto.objects.all()

    if request.method == "POST":
        form = OrdenPedidoForm(request.POST)

        if form.is_valid():
<<<<<<< HEAD
            orden = form.save(commit=False)
            orden.mecanico = request.user.perfil
            orden.save()

            detalles = request.POST.get('detalles_json')
            detalles = json.loads(detalles)

=======
            orden = form.save()

            # Recibir el JSON con detalles enviado desde JS
            detalles = request.POST.get('detalles_json')

            
            detalles = json.loads(detalles)

            # Guardar cada detalle en BD
>>>>>>> staging
            for det in detalles:
                DetalleOrden.objects.create(
                    orden=orden,
                    repuesto_id=det['repuesto_id'],
                    cantidad=det['cantidad'],
                    precio_unitario=det['precio_unitario'],
                )

<<<<<<< HEAD
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
=======
            return redirect('pedidos:lista_ordenes')

    context = {
        'form': form,
        'repuestos': repuestos,
    }
    return render(request, 'crear_orden.html', context)
>>>>>>> staging

@login_required
@user_passes_test(es_mecanico)
# AJAX para obtener el precio de compra del repuesto
def obtener_precio_repuesto(request, repuesto_id):
    rep = Repuesto.objects.get(id=repuesto_id)
    return JsonResponse({'precio': rep.precio_compra})


