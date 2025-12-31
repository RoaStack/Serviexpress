from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Repuesto
from .forms import RepuestoForm
from usuarios.utils import es_admin,es_mecanico_o_admin

# === Listar ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_mecanico_o_admin, login_url='usuarios:login_usuario')
def repuestos_index(request):
    repuestos = Repuesto.objects.all()
    return render(request, "repuestos/ficha_repuestos.html", {"repuestos": repuestos})

# === Crear (solo admin) ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:login_usuario')
def repuesto_crear(request):
    if request.method == "POST":
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto creado exitosamente ✅")
            return redirect("repuestos:ficha_repuestos")
        messages.error(request, "Revisa los campos ❌")
    else:
        form = RepuestoForm()
    return render(request, "repuestos/nuevo_repuesto.html", {"form": form})

@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:dashboard')
def repuesto_editar(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)

    if request.method == "POST":
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto actualizado correctamente ✅")
            return redirect("repuestos:ficha_repuestos")
        messages.error(request, "Problema al actualizar ❌")
    else:
        form = RepuestoForm(instance=repuesto)

    return render(request, "repuestos/editar_repuesto.html", {
        "form": form,
        "repuesto": repuesto,
    })


# === Eliminar ===
@login_required(login_url='usuarios:login_usuario')
@user_passes_test(es_admin, login_url='usuarios:login_usuario')
def repuesto_eliminar(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == "POST":
        repuesto.delete()
        messages.success(request, "Repuesto eliminado exitosamente 🗑️")
        return redirect("repuestos:ficha_repuestos")
    return render(request, "repuestos/confirmar_eliminacion.html", {"repuesto": repuesto})



