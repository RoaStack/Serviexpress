import random
from datetime import datetime
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Reserva, Disponibilidad
from .forms import ReservaForm
from usuarios.models import Usuario


# ================================================================
# 🚗 CREAR UNA NUEVA RESERVA (solo Clientes)
# ================================================================
@login_required
@permission_required('reservas.add_reserva', raise_exception=True)
def crear_reserva(request):
    """
    Permite a los clientes crear una nueva reserva.
    El sistema asigna automáticamente un mecánico disponible (y aleatorio)
    según la fecha, hora y día de la semana de la reserva.
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

            # 🧠 Determinar el día de la semana
            dia_semana = reserva.fecha.strftime("%A").lower()
            dias_map = {
                "monday": "lunes",
                "tuesday": "martes",
                "wednesday": "miercoles",
                "thursday": "jueves",
                "friday": "viernes",
                "saturday": "sabado",
            }
            dia_es = dias_map.get(dia_semana, "lunes")

            # 🔍 Buscar disponibilidades activas para ese día
            disponibilidades = Disponibilidad.objects.filter(
                dia_semana=dia_es, activo=True
            ).select_related("mecanico")

            # 🚫 Excluir mecánicos con reservas en esa fecha y hora
            mecanicos_ocupados = Reserva.objects.filter(
                fecha=reserva.fecha, hora=reserva.hora
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

            # 🎯 Asignar mecánico aleatorio
            mecanico_asignado = random.choice(disponibles)
            reserva.mecanico = mecanico_asignado
            reserva.estado = "pendiente"

            # 💾 Guardar reserva
            reserva.save()
            form.save_m2m()

            messages.success(
                request,
                f"✅ ¡Tu reserva fue creada correctamente! Mecánico asignado: {mecanico_asignado.user.username}."
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
    Muestra las reservas según el rol:
    - Admin: todas las reservas.
    - Cliente: solo las suyas.
    """
    if request.user.is_staff or request.user.is_superuser:
        reservas = Reserva.objects.all().order_by("-fecha", "-hora")
    elif request.user.groups.filter(name="Clientes").exists():
        usuario = get_object_or_404(Usuario, user=request.user)
        reservas = Reserva.objects.filter(cliente=usuario).order_by("-fecha", "-hora")
    else:
        messages.warning(request, "Tu usuario no tiene acceso a esta vista.")
        return redirect("usuarios:dashboard")

    return render(request, "reservas/mis_reservas.html", {"reservas": reservas})


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
# 🧰 CAMBIAR ESTADO (solo Admin o Mecanicos - General)
# ================================================================
@login_required
@permission_required('reservas.change_reserva', raise_exception=True)
def cambiar_estado_reserva(request, pk, nuevo_estado):
    """
    Permite a administradores cambiar el estado general de una reserva.
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
        request, f"✅ Estado de la reserva #{reserva.id} actualizado a {estado_legible}."
    )
    return redirect("reservas:mis_reservas")


# ================================================================
# 🔧 ORDENES ASIGNADAS (solo para Mecánicos)
# ================================================================
@login_required
@permission_required('reservas.view_reserva', raise_exception=True)
def ordenes_asignadas(request):
    """
    Muestra las reservas pendientes asignadas al mecánico actual.
    """
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
    """
    Muestra las reservas en proceso asignadas al mecánico actual.
    """
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
    """
    Muestra las reservas finalizadas del mecánico actual.
    """
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
    - en_proceso → finalizada
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

    messages.success(
        request,
        f"✅ Estado de la reserva #{reserva.id} actualizado a {reserva.get_estado_display()}."
    )
    return redirect("reservas:ordenes_asignadas")
