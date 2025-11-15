from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Repuesto, Carrito, ItemCarrito
from django.http import JsonResponse


@login_required
def ver_repuestos(request):
    repuestos = Repuesto.objects.all()
    return render(request, 'ver_repuestos.html', {'repuestos': repuestos})


@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'ver_carrito.html', {'carrito': carrito})

@login_required
def agregar_al_carrito(request, repuesto_id):
    repuesto = get_object_or_404(Repuesto, id=repuesto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, repuesto=repuesto)
    if not creado:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()

    messages.success(request, f"{repuesto.descripcion} añadido al carrito 🛒")
    return redirect('ecommerce:ver_carrito')


@login_required
def agregar_al_carrito_ajax(request, repuesto_id):
    if request.method == "POST":
        repuesto = get_object_or_404(Repuesto, id=repuesto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, repuesto=repuesto)
        if not creado:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()

        total = sum(i.subtotal for i in carrito.items.all())
        return JsonResponse({
            'success': True,
            'descripcion': repuesto.descripcion,
            'cantidad': item.cantidad,
            'total': total,
            'items': carrito.items.count()
        })
    return JsonResponse({'success': False})



@login_required
def detalle_carrito_ajax(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    html = render_to_string('_detalle_carrito.html', {'carrito': carrito})
    return JsonResponse({'html': html})


@login_required
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.info(request, "Tu carrito ha sido vaciado 🗑️")
    return redirect('ecommerce:ver_repuestos')

@login_required
def generar_comprobante(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if carrito.items.count() == 0:
        messages.warning(request, "Tu carrito está vacío, no puedes generar un comprobante.")
        return redirect('repuestos:ver_repuestos')

    # 🔸 Primero validamos que haya stock suficiente
    for item in carrito.items.all():
        if item.cantidad > item.repuesto.stock:
            messages.error(request, f"No hay stock suficiente de: {item.repuesto.descripcion}")
            return redirect('ecommerce:ver_carrito')

    # 🔸 Descontar stock de cada repuesto
    for item in carrito.items.all():
        repuesto = item.repuesto
        repuesto.stock -= item.cantidad
        repuesto.save()  # Guarda el nuevo stock

    total = carrito.total

    # 🔸 Guardar datos para mostrar en el comprobante ANTES de vaciar el carrito
    items_para_comprobante = list(carrito.items.all())  

    # 🔸 Vaciar carrito después de la compra
    carrito.items.all().delete()

    # 🔸 Enviar datos al template
    return render(request, 'comprobante.html', {
        'items': items_para_comprobante,
        'total': total,
        'usuario': request.user,
        'fecha': timezone.now(),
    })
