import random
from datetime import datetime, timedelta, time
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from .models import Reserva, Disponibilidad
from .forms import ReservaForm
from usuarios.models import Usuario

# 🔹 Importamos modelos y formularios de Boletas
from boletas.models import Boleta, DetalleServicioBoleta, DetalleBoleta
from boletas.forms import DetalleBoletaForm  # 👈 ESTA LÍNEA SOLUCIONA EL ERROR
from repuestos.models import Repuesto
from servicios.models import Servicio


# ================================================================
# 🚗 CREAR UNA NUEVA RESERVA (solo Clientes)
# ================================================================
@login_required
@permission_required('reservas.add_reserva', raise_exception=True)
def crear_reserva(request):
    """
    Permite a los clientes crear una nueva reserva.
    El sistema asigna automáticamente un mecánico disponible (y aleatorio)
    según la fecha y hora seleccionada, evitando feriados y colisiones.
    """
    if not request.user.groups.filter(name="Clientes").exists():
        messages.warning(request, "Solo los clientes pueden crear reservas.")
        return redirect("usuarios:dashboard")

    cliente = get_object_or_404(Usuario, user=request.user)

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente

            # === 🧠 Asignar mecánico automáticamente según disponibilidad ===
            disponibilidades = Disponibilidad.objects.filter(
                fecha=reserva.fecha,
                activo=True
            ).select_related("mecanico")

            mecanicos_ocupados = Reserva.objects.filter(
                fecha=reserva.fecha,
                hora=reserva.hora
            ).values_list("mecanico_id", flat=True)

            disponibles = [
                disp.mecanico for disp in disponibilidades
                if disp.mecanico_id not in mecanicos_ocupados
            ]

            if not disponibles:
                messages.error(
                    request,
                    "❌ No hay mecánicos disponibles para esa fecha y hora. Intenta otro horario."
                )
                return render(request, "reservas/crear_reserva.html", {"form": form})

            mecanico_asignado = random.choice(disponibles)
            reserva.mecanico = mecanico_asignado
            reserva.estado = "pendiente"
            reserva.save()
            form.save_m2m()

            messages.success(
                request,
                f"✅ ¡Tu reserva fue creada correctamente! Mecánico asignado: {mecanico_asignado.user.get_full_name()}."
            )
            return redirect("reservas:mis_reservas")
        else:
            messages.error(request, "Por favor revisa los campos del formulario.")
    else:
        form = ReservaForm()

    return render(request, "reservas/crear_reserva.html", {"form": form})


# ================================================================
# 📋 LISTAR RESERVAS SEGÚN EL TIPO DE USUARIO
# ================================================================
@login_required
@permission_required('reservas.view_reserva', raise_exception=True)
def mis_reservas(request):
    """
    Muestra las reservas activas del cliente (pendientes o en proceso).
    Admin y staff ven todas las reservas activas.
    """
    if request.user.is_staff or request.user.is_superuser:
        reservas = Reserva.objects.exclude(estado="finalizada").order_by("-fecha", "-hora")
    elif request.user.groups.filter(name="Clientes").exists():
        usuario = get_object_or_404(Usuario, user=request.user)
        reservas = Reserva.objects.filter(
            cliente=usuario
        ).exclude(estado="finalizada").order_by("-fecha", "-hora")
    else:
        messages.warning(request, "Tu usuario no tiene acceso a esta vista.")
        return redirect("usuarios:dashboard")

    return render(request, "reservas/mis_reservas.html", {"reservas": reservas})


@login_required
@permission_required('reservas.view_reserva', raise_exception=True)
def servicios_realizados_cliente(request):
    """
    Muestra solo las últimas reservas finalizadas del cliente (más recientes primero).
    Se limitan a las 10 más recientes para evitar una lista demasiado larga.
    """
    if not request.user.groups.filter(name="Clientes").exists():
        messages.warning(request, "Solo los clientes pueden acceder a esta vista.")
        return redirect("usuarios:dashboard")

    usuario = get_object_or_404(Usuario, user=request.user)
    reservas = (
        Reserva.objects.filter(cliente=usuario, estado="finalizada")
        .order_by("-fecha", "-hora")[:10]  # 👈 Solo muestra las 10 más recientes
    )

    return render(request, "reservas/servicios_realizados_cliente.html", {"reservas": reservas})





# ================================================================
# ❌ CANCELAR UNA RESERVA (solo Clientes)
# ================================================================
@login_required
@permission_required('reservas.change_reserva', raise_exception=True)
def cancelar_reserva(request, pk):
    usuario = get_object_or_404(Usuario, user=request.user)
    reserva = get_object_or_404(Reserva, id=pk, cliente=usuario)

    if reserva.estado == "pendiente":
        reserva.estado = "cancelada"
        reserva.save()
        messages.info(request, "🗓️ Tu reserva fue cancelada con éxito.")
    else:
        messages.warning(
            request,
            "No puedes cancelar una reserva ya en proceso o finalizada."
        )

    return redirect("reservas:mis_reservas")


# ================================================================
# 🧰 CAMBIAR ESTADO (solo Admin o Mecanicos)
# ================================================================
@login_required
@permission_required('reservas.change_reserva', raise_exception=True)
def cambiar_estado_reserva(request, pk, nuevo_estado):
    reserva = get_object_or_404(Reserva, id=pk)
    estados_validos = ["pendiente", "en_proceso", "finalizada", "cancelada"]

    if nuevo_estado not in estados_validos:
        messages.error(request, "Estado no válido.")
        return redirect("reservas:mis_reservas")

    reserva.estado = nuevo_estado
    reserva.save()

    estado_legible = nuevo_estado.replace("_", " ").capitalize()
    messages.success(
        request, f"✅ Estado de la reserva #{reserva.id} actualizado a {estado_legible}."
    )
    return redirect("reservas:mis_reservas")


# ================================================================
# 🔧 ORDENES ASIGNADAS (solo para Mecánicos)
# ================================================================
@login_required
@permission_required('reservas.view_reserva', raise_exception=True)
def ordenes_asignadas(request):
    if not request.user.groups.filter(name="Mecanicos").exists():
        messages.warning(request, "Solo los mecánicos pueden acceder a esta vista.")
        return redirect("usuarios:dashboard")

    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = Reserva.objects.filter(
        mecanico=mecanico, estado="pendiente"
    ).order_by("fecha", "hora")

    return render(request, "reservas/ordenes_asignadas.html", {"reservas": reservas})


# ================================================================
# ⚙️ SERVICIOS EN PROCESO (solo para Mecánicos)
# ================================================================
@login_required
@permission_required('reservas.change_reserva', raise_exception=True)
def servicios_en_proceso(request):
    if not request.user.groups.filter(name="Mecanicos").exists():
        messages.warning(request, "Solo los mecánicos pueden acceder a esta vista.")
        return redirect("usuarios:dashboard")

    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = Reserva.objects.filter(
        mecanico=mecanico, estado="en_proceso"
    ).order_by("fecha", "hora")

    return render(request, "reservas/servicios_en_proceso.html", {"reservas": reservas})


# ================================================================
# 📜 HISTORIAL DE SERVICIOS (solo para Mecánicos)
# ================================================================
@login_required
@permission_required('reservas.view_reserva', raise_exception=True)
def historial_servicios(request):
    if not request.user.groups.filter(name="Mecanicos").exists():
        messages.warning(request, "Solo los mecánicos pueden acceder a esta vista.")
        return redirect("usuarios:dashboard")

    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = Reserva.objects.filter(
        mecanico=mecanico, estado="finalizada"
    ).order_by("-fecha", "-hora")

    return render(request, "reservas/historial_servicios.html", {"reservas": reservas})


# ================================================================
# 🔁 CAMBIAR ESTADO DE RESERVAS (solo para Mecánicos)
# ================================================================
@login_required
@permission_required('reservas.change_reserva', raise_exception=True)
def actualizar_estado_mecanico(request, pk, nuevo_estado):
    """
    Permite al mecánico cambiar el estado de sus reservas:
    - pendiente → en_proceso
    - en_proceso → finalizada (y genera boleta)
    """
    if not request.user.groups.filter(name="Mecanicos").exists():
        messages.warning(request, "No tienes permisos para esta acción.")
        return redirect("usuarios:dashboard")

    mecanico = get_object_or_404(Usuario, user=request.user)
    reserva = get_object_or_404(Reserva, pk=pk, mecanico=mecanico)

    transiciones_validas = {
        "pendiente": ["en_proceso"],
        "en_proceso": ["finalizada"],
    }

    if nuevo_estado not in transiciones_validas.get(reserva.estado, []):
        messages.error(request, "Cambio de estado no permitido.")
        return redirect("reservas:ordenes_asignadas")

    reserva.estado = nuevo_estado
    reserva.save()

    # 🔥 Si pasa a finalizada, generar la boleta automáticamente
    if nuevo_estado == "finalizada":
        boleta, creada = Boleta.objects.get_or_create(
            reserva=reserva,
            defaults={"cliente": reserva.cliente}
        )

        # Asociar servicios de la reserva
        for servicio in reserva.servicios.all():
            DetalleServicioBoleta.objects.create(
                boleta=boleta,
                servicio=servicio,
                precio_servicio=servicio.precio
            )

        # Recalcular total
        boleta.calcular_total()

        messages.success(
            request,
            f"✅ Reserva finalizada correctamente. Se generó la boleta #{boleta.id}."
        )

        # 🔁 Redirigir directamente al historial de servicios
        return redirect("reservas:historial_servicios")

    else:
        messages.success(
            request,
            f"✅ Estado de la reserva #{reserva.id} actualizado a {reserva.get_estado_display()}."
        )
        return redirect("reservas:ordenes_asignadas")





@login_required
def obtener_horas_disponibles(request):
    """
    Devuelve las horas disponibles según la fecha seleccionada.
    - Excluye las horas dentro del rango de colación.
    - Excluye bloques ya reservados.
    """
    fecha_str = request.GET.get("fecha")
    if not fecha_str:
        return JsonResponse({"error": "No se envió la fecha."}, status=400)

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Formato de fecha inválido."}, status=400)

    disponibilidades = Disponibilidad.objects.filter(fecha=fecha, activo=True)
    horas_disponibles = set()

    for disp in disponibilidades:
        hora_actual = datetime.combine(fecha, disp.hora_inicio)
        hora_fin = datetime.combine(fecha, disp.hora_termino)
        bloque = timedelta(minutes=disp.duracion_bloque)

        while hora_actual + bloque <= hora_fin:
            hora = hora_actual.time()

            # 🚫 Excluir horas dentro del rango de colación
            if disp.colacion_inicio <= hora < disp.colacion_termino:
                hora_actual += bloque
                continue

            # 🚫 Excluir horas ya reservadas
            if Reserva.objects.filter(
                fecha=fecha,
                hora=hora,
                mecanico=disp.mecanico,
                estado__in=["pendiente", "en_proceso"]
            ).exists():
                hora_actual += bloque
                continue

            horas_disponibles.add(hora.strftime("%H:%M"))
            hora_actual += bloque

    horas_ordenadas = sorted(list(horas_disponibles))
    return JsonResponse({"horas": horas_ordenadas})


@login_required
@permission_required('boletas.add_detalleboleta', raise_exception=True)
def registrar_repuestos_reserva(request, reserva_id):
    """
    Agrega repuestos a la reserva. Si no existe boleta, la crea.
    Descuenta stock UNA sola vez (aquí).
    """
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    # Boleta on-demand (sin finalizar la reserva)
    boleta, _ = Boleta.objects.get_or_create(
        reserva=reserva,
        defaults={"cliente": reserva.cliente}
    )

    form = DetalleBoletaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        detalle = form.save(commit=False)
        detalle.boleta = boleta

        repuesto = detalle.repuesto
        cantidad = detalle.cantidad

        # Validar stock y descontar SOLO aquí
        if cantidad > repuesto.stock:
            messages.error(request, f"❌ Stock insuficiente de {repuesto.descripcion}. Disponible: {repuesto.stock}.")
            return redirect("reservas:registrar_repuestos_reserva", reserva_id=reserva.id)

        # Asignar precio del catálogo y persistir
        detalle.precio_unitario = repuesto.precio_venta
        detalle.save()

        # Descontar stock y recalcular total
        repuesto.stock -= cantidad
        repuesto.save()
        boleta.calcular_total()

        messages.success(request, f"✅ Se agregó {cantidad}× {repuesto.descripcion} correctamente.")
        return redirect("reservas:registrar_repuestos_reserva", reserva_id=reserva.id)

    detalles = boleta.detalles_repuestos.all()
    total_repuestos = sum(d.subtotal() for d in detalles)

    return render(request, "reservas/registrar_repuestos_reserva.html", {
        "reserva": reserva,
        "boleta": boleta,
        "form": form,
        "detalles": detalles,
        "total_repuestos": total_repuestos,
    })


@login_required
@permission_required('boletas.delete_detalleboleta', raise_exception=True)
def eliminar_repuesto_detalle(request, reserva_id, detalle_id):
    """
    Elimina un repuesto de una boleta y devuelve su stock a la base de datos.
    """
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    detalle = get_object_or_404(DetalleBoleta, pk=detalle_id, boleta__reserva=reserva)

    if request.method == "POST":
        repuesto = detalle.repuesto
        cantidad_devuelta = detalle.cantidad

        # ✅ Devolver el stock
        repuesto.stock += cantidad_devuelta
        repuesto.save()

        # ✅ Eliminar el detalle y recalcular total
        boleta = detalle.boleta
        detalle.delete()
        boleta.calcular_total()

        messages.success(request, f"♻️ Se eliminó '{repuesto.descripcion}' y se devolvieron {cantidad_devuelta} unidades al stock.")
    else:
        messages.error(request, "Operación no permitida.")

    return redirect("reservas:registrar_repuestos_reserva", reserva_id=reserva.id)
