from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from .forms import RegistroClienteForm, EditarPerfilForm
from .models import Usuario
from django.http import JsonResponse
import json
from .forms import RegistroMecanicoForm, EditarMecanicoForm   # los creas tú, similar a RegistroClienteForm



# 🧩 Registro de clientes (desde la web)
def registro_cliente(request):
    if request.method == "POST":
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_cliente, _ = Group.objects.get_or_create(name="Clientes")
            user.groups.add(grupo_cliente)
            login(request, user)
            messages.success(request, "¡Tu cuenta fue creada con éxito! 🎉")
            return redirect("usuarios:dashboard")
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistroClienteForm()

    return render(request, "usuarios/registro.html", {"form": form})


# 🔐 Login
def login_usuario(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido {user.username}")
                return redirect("usuarios:dashboard")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Datos inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, "usuarios/login.html", {"form": form})


# 🚪 Logout
@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("usuarios:login_usuario")


# 🧭 Dashboard dinámico según grupo
@login_required
def dashboard(request):
    user = request.user

    # 👑 Admin (staff o superuser)
    if user.is_staff or user.is_superuser:
        return render(request, "usuarios/administrador/dashboard_admin.html")

    # 🔧 Mecánico
    if user.groups.filter(name="Mecanicos").exists():
        return render(request, "usuarios/mecanico/dashboard_mecanico.html")

    # 👤 Cliente
    if user.groups.filter(name="Clientes").exists():
        return render(request, "usuarios/cliente/dashboard_cliente.html")

    # Si no pertenece a ningún grupo
    messages.warning(request, "Tu usuario no tiene un rol asignado. Contacta al administrador.")
    return redirect("usuarios:login_usuario")


@login_required
def ver_perfil(request):
    user = request.user
    grupo = None

    if user.is_staff or user.is_superuser:
        grupo = "Administrador"
        template = "usuarios/administrador/ver_perfil.html"
    elif user.groups.filter(name="Mecanicos").exists():
        grupo = "Mecánico"
        template = "usuarios/mecanico/ver_perfil.html"
    elif user.groups.filter(name="Clientes").exists():
        grupo = "Cliente"
        template = "usuarios/cliente/ver_perfil.html"
    else:
        messages.warning(request, "No tienes un rol asignado. Contacta al administrador.")
        return redirect("usuarios:dashboard")

    return render(request, template, {"user": user, "grupo": grupo})
@login_required
def editar_perfil(request):
    user = request.user
    perfil = getattr(user, "perfil", None)

    if request.method == "POST" and request.headers.get("Content-Type") == "application/json":
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")

        # Validar y actualizar según el campo
        if hasattr(user, field):
            setattr(user, field, value)
            user.save()
        elif hasattr(perfil, field):
            setattr(perfil, field, value)
            perfil.save()
        else:
            return JsonResponse({"success": False})

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def es_admin(user):
    # Ajusta esta función a tu lógica real de admin
    return user.is_staff or user.groups.filter(name="Admin").exists()


# usuarios/views.py

@login_required
@user_passes_test(es_admin, login_url="usuarios:dashboard")
def gestion_mecanicos(request):
    mecanicos = (
        Usuario.objects
        .filter(user__groups__name="Mecanicos")
        .select_related("user")
        .order_by("user__username")
    )
    contexto = {
        "mecanicos": mecanicos,
        "total_mecanicos": mecanicos.count(),
    }
    # 👇 CAMBIA ESTA LÍNEA
    return render(request, "usuarios/administrador/gestion_mecanicos.html", contexto)


@login_required
@user_passes_test(es_admin, login_url="usuarios:dashboard")
def crear_mecanico(request):
    if request.method == "POST":
        form = RegistroMecanicoForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_mecanicos, _ = Group.objects.get_or_create(name="Mecanicos")
            user.groups.add(grupo_mecanicos)
            messages.success(request, "✅ Mecánico creado correctamente.")
            return redirect("usuarios:gestion_mecanicos")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = RegistroMecanicoForm()

    # 👇 CAMBIA ESTA LÍNEA
    return render(request, "usuarios/administrador/crear_mecanico.html", {"form": form})


@login_required
@user_passes_test(es_admin, login_url="usuarios:dashboard")
def editar_mecanico(request, usuario_id):
    mecanico = get_object_or_404(
        Usuario,
        id=usuario_id,
        user__groups__name="Mecanicos"
    )

    if request.method == "POST":
        form = EditarMecanicoForm(request.POST, instance=mecanico)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Datos del mecánico actualizados.")
            return redirect("usuarios:gestion_mecanicos")
        else:
            messages.error(request, "Corrige los errores del formulario.")
    else:
        form = EditarMecanicoForm(instance=mecanico)

    # 👇 CAMBIA ESTA LÍNEA
    return render(
        request,
        "usuarios/administrador/editar_mecanico.html",
        {"form": form, "mecanico": mecanico},
    )


@login_required
@user_passes_test(es_admin, login_url="usuarios:dashboard")
def eliminar_mecanico(request, usuario_id):
    mecanico = get_object_or_404(
        Usuario,
        id=usuario_id,
        user__groups__name="Mecanicos"
    )

    if request.method == "POST":
        nombre = mecanico.user.username
        mecanico.user.delete()
        messages.success(request, f"🗑️ Mecánico '{nombre}' eliminado correctamente.")
        return redirect("usuarios:gestion_mecanicos")

    # Si quieres una página de confirmación:
    return render(
        request,
        "usuarios/administrador/confirmar_eliminar_mecanico.html",
        {"mecanico": mecanico},
    )
