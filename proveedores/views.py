from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Proveedor
from .forms import ProveedorForm

# --- Permisos ---
def es_admin(user):
    return user.is_staff or user.is_superuser

def es_mecanico(user):
    return user.is_authenticated and user.groups.filter(name='mecanico').exists()

def puede_ver_proveedores(user):
    return es_admin(user) or es_mecanico(user)

# === Listar (admin y mecánico) ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(puede_ver_proveedores, login_url='usuarios:login_usuario')
def proveedores_index(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedores/ficha_proveedores.html", {"proveedores": proveedores})

# === Crear (solo admin) ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:login_usuario')
def proveedor_crear(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado exitosamente ✅")
            return redirect("proveedores:ficha_proveedores")
        messages.error(request, "Revisa los campos del formulario ❌")
    else:
        form = ProveedorForm()
    return render(request, "proveedores/nuevo_proveedor.html", {"form": form})

# === Editar Proveedor (solo admin) ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:dashboard')
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente ✅")
            return redirect("proveedores:ficha_proveedores")
        else:
            messages.error(request, "No se pudo actualizar. Verifica los datos ❌")
    else:
        form = ProveedorForm(instance=proveedor)

    return render(
        request,
        "proveedores/editar_proveedor.html",
        {
            "form": form,
            "proveedor": proveedor,
        }
    )



# === Eliminar (solo admin) ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:login_usuario')
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == "POST":
        proveedor.delete()
        messages.success(request, "Proveedor eliminado exitosamente 🗑️")
        return redirect("proveedores:ficha_proveedores")
    return render(request, "proveedores/confirmar_eliminacion.html", {"proveedor": proveedor})

