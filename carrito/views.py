from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Repuesto, Carrito, ItemCarrito, Compra, CompraItem
from django.http import JsonResponse

def es_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Clientes').exists()


@login_required
@user_passes_test(es_cliente)
def ver_repuestos(request):
    repuestos = Repuesto.objects.all()
    return render(request, 'ver_repuestos.html', {'repuestos': repuestos})


@login_required
@user_passes_test(es_cliente)
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return render(request, 'ver_carrito.html', {'carrito': carrito})

@login_required
@user_passes_test(es_cliente)
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

    messages.success(request, f"{repuesto.nombre} añadido al carrito 🛒")
    return redirect('ecommerce:ver_carrito')


@login_required
@user_passes_test(es_cliente)
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
            'nombre': repuesto.nombre,
            'cantidad': item.cantidad,
            'total': total,
            'items': carrito.items.count()
        })
    return JsonResponse({'success': False})



@login_required
@user_passes_test(es_cliente)
def detalle_carrito_ajax(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    html = render_to_string('_detalle_carrito.html', {'carrito': carrito})
    return JsonResponse({'html': html})


@login_required
@user_passes_test(es_cliente)
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.info(request, "Tu carrito ha sido vaciado 🗑️")
    return redirect('ecommerce:ver_repuestos')

@login_required
@user_passes_test(es_cliente)
def generar_comprobante(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if carrito.items.count() == 0:
        messages.warning(request, "Tu carrito está vacío, no puedes generar un comprobante.")
        return redirect('ecommerce:ver_carrito')

    # Validar stock
    for item in carrito.items.all():
        if item.cantidad > item.repuesto.stock:
            messages.error(request, f"No hay stock suficiente de: {item.repuesto.nombre}")
            return redirect('ecommerce:ver_carrito')

    # Descontar stock
    for item in carrito.items.all():
        repuesto = item.repuesto
        repuesto.stock -= item.cantidad
        repuesto.save()

    # Crear la Compra
    compra = Compra.objects.create(
        usuario=request.user,
        total=carrito.total
    )

    # Crear los CompraItem
    items_para_comprobante = []

    for item in carrito.items.all():
        compra_item = CompraItem.objects.create(
            compra=compra,
            repuesto=item.repuesto,
            cantidad=item.cantidad,
            precio_unitario=item.repuesto.precio_venta
        )
        items_para_comprobante.append(compra_item)

    # Vaciar carrito
    carrito.items.all().delete()

    # Renderizar comprobante
    return render(request, 'comprobante.html', {
        'items': items_para_comprobante,
        'total': compra.total,
        'usuario': request.user,
        'fecha': compra.fecha,
    })

@login_required
@user_passes_test(es_cliente)
def mis_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, "mis_compras.html", {
        "compras": compras
    })


@login_required
@user_passes_test(es_cliente)
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    items = compra.items.all() 

    contexto = {
        "usuario": request.user,
        "fecha": compra.fecha,
        "items": items,
        "total": compra.total
    }

    return render(request, "comprobante.html", contexto)


