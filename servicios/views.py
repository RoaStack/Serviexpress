from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Servicio
from .forms import ServicioForm
from usuarios.utils import es_admin

@login_required
@user_passes_test(es_admin)
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio creado exitosamente ✅")
            return redirect('servicios:listar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'crear_servicio.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def listar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'listar_servicios.html', {'servicios': servicios})


@login_required
@user_passes_test(es_admin)
def editar_servicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente ✅")
            return redirect('servicios:listar_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'editar_servicio.html', {'form': form, 'servicio': servicio})


@login_required
@user_passes_test(es_admin)
def eliminar_servicio(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, "Servicio eliminado exitosamente 🗑️")
        return redirect('servicios:listar_servicios')
    return render(request, 'confirmar_eliminacion.html', {'servicio': servicio})

