from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .forms import OrdenPedidoForm
from .models import DetalleOrden
from repuestos.models import Repuesto
import json


def es_mecanico(user):
    return user.is_authenticated and user.groups.filter(name='Mecanicos').exists()


@login_required
@user_passes_test(es_mecanico)
def crear_orden(request):
    form = OrdenPedidoForm()
    repuestos = Repuesto.objects.all()

    if request.method == "POST":
        form = OrdenPedidoForm(request.POST)

        if form.is_valid():
            orden = form.save()

            # Recibir el JSON con detalles enviado desde JS
            detalles = request.POST.get('detalles_json')

            
            detalles = json.loads(detalles)

            # Guardar cada detalle en BD
            for det in detalles:
                DetalleOrden.objects.create(
                    orden=orden,
                    repuesto_id=det['repuesto_id'],
                    cantidad=det['cantidad'],
                    precio_unitario=det['precio_unitario'],
                )

            return redirect('pedidos:lista_ordenes')

    context = {
        'form': form,
        'repuestos': repuestos,
    }
    return render(request, 'crear_orden.html', context)

@login_required
@user_passes_test(es_mecanico)
# AJAX para obtener el precio de compra del repuesto
def obtener_precio_repuesto(request, repuesto_id):
    rep = Repuesto.objects.get(id=repuesto_id)
    return JsonResponse({'precio': rep.precio_compra})


