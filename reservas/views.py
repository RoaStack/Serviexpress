import random
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReservaForm
from .models import Disponibilidad, Reserva
from usuarios.models import Usuario
from boletas.models import Boleta, DetalleBoleta, DetalleServicioBoleta
from boletas.forms import DetalleBoletaForm
from django.db import transaction
from .forms import ReservaForm, DisponibilidadMasivaForm

# ================================================================
# 🔐 HELPERS DE ROLES
# ================================================================
def es_cliente(user):
    return user.is_authenticated and user.groups.filter(name="Clientes").exists()


def es_mecanico(user):
    return user.is_authenticated and user.groups.filter(name="Mecanicos").exists()


def es_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def es_cliente_o_admin(user):
    return es_cliente(user) or es_admin(user)


def es_mecanico_o_admin(user):
    return es_mecanico(user) or es_admin(user)


# ================================================================
# 👤 VISTAS PARA CLIENTES
# ================================================================

# 🚗 CREAR UNA NUEVA RESERVA (solo Clientes)
@login_required
@permission_required("reservas.add_reserva", raise_exception=True)
@user_passes_test(es_cliente, login_url="usuarios:dashboard")
def crear_reserva(request):
    """
    Permite a los clientes crear una nueva reserva.
    El sistema asigna automáticamente un mecánico disponible (y aleatorio)
    según la fecha y hora seleccionadas.
    """
    cliente = get_object_or_404(Usuario, user=request.user)

    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.cliente = cliente

            # === Asignar mecánico automáticamente según disponibilidad ===
            disponibilidades = (
                Disponibilidad.objects.filter(fecha=reserva.fecha, activo=True)
                .select_related("mecanico")
            )

            mecanicos_ocupados = Reserva.objects.filter(
                fecha=reserva.fecha,
                hora=reserva.hora,
                estado__in=["pendiente", "en_proceso"],
            ).values_list("mecanico_id", flat=True)

            disponibles = [
                disp.mecanico
                for disp in disponibilidades
                if disp.mecanico_id not in mecanicos_ocupados
            ]

            if not disponibles:
                messages.error(
                    request,
                    "❌ No hay mecánicos disponibles para esa fecha y hora. "
                    "Intenta otro horario.",
                )
                return render(
                    request,
                    "reservas/reservas_cliente/crear_reserva.html",
                    {"form": form},
                )

            mecanico_asignado = random.choice(disponibles)
            reserva.mecanico = mecanico_asignado
            reserva.estado = "pendiente"
            reserva.save()
            form.save_m2m()

            messages.success(
                request,
                "✅ ¡Tu reserva fue creada correctamente! "
                f"Mecánico asignado: {mecanico_asignado.user.get_full_name()}.",
            )
            return redirect("reservas:mis_reservas")

        messages.error(request, "Por favor revisa los campos del formulario.")
    else:
        form = ReservaForm()

    return render(
        request,
        "reservas/reservas_cliente/crear_reserva.html",
        {"form": form},
    )




# 📋 LISTAR RESERVAS (Clientes y Admin/Staff)
@login_required
@permission_required("reservas.view_reserva", raise_exception=True)
@user_passes_test(es_cliente_o_admin, login_url="usuarios:dashboard")
def mis_reservas(request):
    """
    - Admin/Staff: ven todas las reservas no finalizadas.
    - Cliente: ve solo sus reservas no finalizadas.
    """
    if es_admin(request.user):
        reservas = (
            Reserva.objects.exclude(estado="finalizada")
            .order_by("-fecha", "-hora")
        )
    else:  # Cliente
        usuario = get_object_or_404(Usuario, user=request.user)
        reservas = (
            Reserva.objects.filter(cliente=usuario)
            .exclude(estado="finalizada")
            .order_by("-fecha", "-hora")
        )

    return render(request, "reservas/reservas_cliente/mis_reservas.html", {"reservas": reservas})


# 🧾 SERVICIOS REALIZADOS (Historial cliente)
@login_required
@permission_required("reservas.view_reserva", raise_exception=True)
@user_passes_test(es_cliente, login_url="usuarios:dashboard")
def servicios_realizados_cliente(request):
    """
    Muestra solo las últimas reservas finalizadas del cliente (máx. 10).
    """
    usuario = get_object_or_404(Usuario, user=request.user)
    reservas = (
        Reserva.objects.filter(cliente=usuario, estado="finalizada")
        .order_by("-fecha", "-hora")[:10]
    )

    return render(
        request,
        "reservas/reservas_cliente/servicios_realizados_cliente.html",
        {"reservas": reservas},
    )


# ❌ CANCELAR RESERVA (solo Cliente)
@login_required
@permission_required("reservas.change_reserva", raise_exception=True)
@user_passes_test(es_cliente, login_url="usuarios:dashboard")
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
            "No puedes cancelar una reserva que ya está en proceso o finalizada.",
        )

    return redirect("reservas:mis_reservas")


# 🕒 HORAS DISPONIBLES (AJAX para Cliente)
@login_required
@user_passes_test(es_cliente, login_url="usuarios:dashboard")
def obtener_horas_disponibles(request):
    """
    Devuelve las horas disponibles según la fecha seleccionada.
    - Excluye horas dentro del rango de colación.
    - Excluye bloques ya reservados.
    """
    fecha_str = request.GET.get("fecha")
    if not fecha_str:
        return JsonResponse({"error": "No se envió la fecha."}, status=400)

    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"error": "Formato de fecha inválido."}, status=400)

    disponibilidades = (
        Disponibilidad.objects.filter(fecha=fecha, activo=True)
        .select_related("mecanico")
    )

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

            # 🚫 Excluir horas ocupadas SOLO por reservas activas
            if Reserva.objects.filter(
                fecha=fecha,
                hora=hora,
                mecanico=disp.mecanico,
                estado__in=["pendiente", "en_proceso"]  # <- FIX IMPORTANTE
            ).exists():
                hora_actual += bloque
                continue

            horas_disponibles.add(hora.strftime("%H:%M"))
            hora_actual += bloque

    horas_ordenadas = sorted(horas_disponibles)
    return JsonResponse({"horas": horas_ordenadas})



# ================================================================
# 🔧 VISTAS PARA MECÁNICOS / ADMIN
# ================================================================

# 🧰 CAMBIAR ESTADO (Admin o Mecánico)
@login_required
@permission_required("reservas.change_reserva", raise_exception=True)
@user_passes_test(es_mecanico_o_admin, login_url="usuarios:dashboard")
def cambiar_estado_reserva(request, pk, nuevo_estado):
    """
    Cambia el estado de una reserva (usuarios con permiso y rol válido).
    """
    reserva = get_object_or_404(Reserva, id=pk)
    estados_validos = ["pendiente", "en_proceso", "finalizada", "cancelada"]

    if nuevo_estado not in estados_validos:
        messages.error(request, "Estado no válido.")
        return redirect("reservas:mis_reservas")

    reserva.estado = nuevo_estado
    reserva.save()

    estado_legible = nuevo_estado.replace("_", " ").capitalize()
    messages.success(
        request,
        f"✅ Estado de la reserva #{reserva.id} actualizado a {estado_legible}.",
    )
    return redirect("reservas:mis_reservas")


# 🔧 ÓRDENES ASIGNADAS (solo Mecánico)
@login_required
@permission_required("reservas.view_reserva", raise_exception=True)
@user_passes_test(es_mecanico, login_url="usuarios:dashboard")
def ordenes_asignadas(request):
    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = (
        Reserva.objects.filter(mecanico=mecanico, estado="pendiente")
        .order_by("fecha", "hora")
    )

    return render(
        request,
        "reservas/reservas_mecanico/ordenes_asignadas.html",
        {"reservas": reservas},
    )


# ⚙️ SERVICIOS EN PROCESO (solo Mecánico)
@login_required
@permission_required("reservas.change_reserva", raise_exception=True)
@user_passes_test(es_mecanico, login_url="usuarios:dashboard")
def servicios_en_proceso(request):
    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = (
        Reserva.objects.filter(mecanico=mecanico, estado="en_proceso")
        .order_by("fecha", "hora")
    )

    return render(
        request,
        "reservas/reservas_mecanico/servicios_en_proceso.html",
        {"reservas": reservas},
    )


# 📜 HISTORIAL DE SERVICIOS (solo Mecánico)
@login_required
@permission_required("reservas.view_reserva", raise_exception=True)
@user_passes_test(es_mecanico, login_url="usuarios:dashboard")
def historial_servicios(request):
    mecanico = get_object_or_404(Usuario, user=request.user)
    reservas = (
        Reserva.objects.filter(mecanico=mecanico, estado="finalizada")
        .order_by("-fecha", "-hora")
    )

    return render(
        request,
        "reservas/reservas_mecanico/historial_servicios.html",
        {"reservas": reservas},
    )


# 🔁 CAMBIAR ESTADO DESDE PANEL MECÁNICO
@login_required
@permission_required("reservas.change_reserva", raise_exception=True)
@user_passes_test(es_mecanico, login_url="usuarios:dashboard")
def actualizar_estado_mecanico(request, pk, nuevo_estado):
    """
    Permite al mecánico cambiar el estado de sus reservas:
    - pendiente → en_proceso
    - en_proceso → finalizada (y genera boleta)
    """
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

    # Si pasa a finalizada, generar la boleta automáticamente
    if nuevo_estado == "finalizada":
        boleta, creada = Boleta.objects.get_or_create(
            reserva=reserva,
            defaults={"cliente": reserva.cliente},
        )

        for servicio in reserva.servicios.all():
            DetalleServicioBoleta.objects.create(
                boleta=boleta,
                servicio=servicio,
                precio_servicio=servicio.precio,
            )

        boleta.calcular_total()

        messages.success(
            request,
            f"✅ Reserva finalizada correctamente. Se generó la boleta #{boleta.id}.",
        )
        return redirect("reservas:historial_servicios")

    messages.success(
        request,
        f"✅ Estado de la reserva #{reserva.id} "
        f"actualizado a {reserva.get_estado_display()}.",
    )
    return redirect("reservas:ordenes_asignadas")


# 🧾 REGISTRAR REPUESTOS EN UNA RESERVA (Mecánico o Admin)
@login_required
@permission_required("boletas.add_detalleboleta", raise_exception=True)
@user_passes_test(es_mecanico_o_admin, login_url="usuarios:dashboard")
def registrar_repuestos_reserva(request, reserva_id):
    """
    Agrega repuestos a la reserva. Si no existe boleta, la crea.
    Descuenta stock UNA sola vez (aquí).
    """
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    boleta, _ = Boleta.objects.get_or_create(
        reserva=reserva,
        defaults={"cliente": reserva.cliente},
    )

    form = DetalleBoletaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        detalle = form.save(commit=False)
        detalle.boleta = boleta

        repuesto = detalle.repuesto
        cantidad = detalle.cantidad

        if cantidad > repuesto.stock:
            messages.error(
                request,
                f"❌ Stock insuficiente de {repuesto.descripcion}. "
                f"Disponible: {repuesto.stock}.",
            )
            return redirect(
                "reservas:registrar_repuestos_reserva",
                reserva_id=reserva.id,
            )

        detalle.precio_unitario = repuesto.precio_venta
        detalle.save()

        repuesto.stock -= cantidad
        repuesto.save()
        boleta.calcular_total()

        messages.success(
            request,
            f"✅ Se agregó {cantidad}× {repuesto.descripcion} correctamente.",
        )
        return redirect(
            "reservas:registrar_repuestos_reserva",
            reserva_id=reserva.id,
        )

    detalles = boleta.detalles_repuestos.all()
    total_repuestos = sum(d.subtotal() for d in detalles)

    return render(
        request,
        "reservas/reservas_mecanico/registrar_repuestos_reserva.html",
        {
            "reserva": reserva,
            "boleta": boleta,
            "form": form,
            "detalles": detalles,
            "total_repuestos": total_repuestos,
        },
    )


# ♻️ ELIMINAR REPUESTO DE UNA BOLETA (Mecánico o Admin)
@login_required
@permission_required("boletas.delete_detalleboleta", raise_exception=True)
@user_passes_test(es_mecanico_o_admin, login_url="usuarios:dashboard")
def eliminar_repuesto_detalle(request, reserva_id, detalle_id):
    """
    Elimina un repuesto de una boleta y devuelve su stock a la base de datos.
    """
    reserva = get_object_or_404(Reserva, pk=reserva_id)
    detalle = get_object_or_404(
        DetalleBoleta,
        pk=detalle_id,
        boleta__reserva=reserva,
    )

    if request.method == "POST":
        repuesto = detalle.repuesto
        cantidad_devuelta = detalle.cantidad

        repuesto.stock += cantidad_devuelta
        repuesto.save()

        boleta = detalle.boleta
        detalle.delete()
        boleta.calcular_total()

        messages.success(
            request,
            f"♻️ Se eliminó '{repuesto.descripcion}' y se devolvieron "
            f"{cantidad_devuelta} unidades al stock.",
        )
    else:
        messages.error(request, "Operación no permitida.")

    return redirect("reservas:registrar_repuestos_reserva", reserva_id=reserva.id)




@login_required
@user_passes_test(es_admin, login_url="usuarios:dashboard")
def crear_disponibilidades_masivas(request):
    """
    Permite al administrador crear disponibilidades para un mecánico
    en un rango de fechas y días de la semana, reutilizando mismos horarios.
    """
    form = DisponibilidadMasivaForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        mecanico = form.cleaned_data["mecanico"]
        fecha_inicio = form.cleaned_data["fecha_inicio"]
        fecha_fin = form.cleaned_data["fecha_fin"]
        dias_semana = list(map(int, form.cleaned_data["dias_semana"]))

        hora_inicio = form.cleaned_data["hora_inicio"]
        hora_termino = form.cleaned_data["hora_termino"]
        colacion_inicio = form.cleaned_data["colacion_inicio"]
        colacion_termino = form.cleaned_data["colacion_termino"]
        duracion_bloque = form.cleaned_data["duracion_bloque"]

        from datetime import timedelta

        creados = 0
        fecha_actual = fecha_inicio

        with transaction.atomic():
            while fecha_actual <= fecha_fin:
                # weekday(): 0 = lunes ... 6 = domingo
                if fecha_actual.weekday() in dias_semana:
                    # evitar duplicar disponibilidades para mismo mecánico y día
                    existe = Disponibilidad.objects.filter(
                        mecanico=mecanico,
                        fecha=fecha_actual,
                        activo=True
                    ).exists()

                    if not existe:
                        Disponibilidad.objects.create(
                            mecanico=mecanico,
                            fecha=fecha_actual,
                            hora_inicio=hora_inicio,
                            hora_termino=hora_termino,
                            colacion_inicio=colacion_inicio,
                            colacion_termino=colacion_termino,
                            duracion_bloque=duracion_bloque,
                            activo=True,
                        )
                        creados += 1

                fecha_actual += timedelta(days=1)

        messages.success(
            request,
            f"✅ Se crearon {creados} disponibilidades nuevas para {mecanico.user.get_full_name()}."
        )
        # Rediriges a la misma vista para que el form vuelva vacío
        return redirect("reservas:crear_disponibilidades_masivas")

    return render(
        request,
        "reservas/reservas_admin/crear_disponibilidades_masivas.html",
        {"form": form},
    )
