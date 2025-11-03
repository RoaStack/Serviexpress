from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render
from .models import Repuesto
from .forms import RepuestoForm

# Helper para restringir solo a administradores
def es_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(es_admin)
def registrar_repuesto(request):
    if request.method == 'POST':
        form = RepuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto ingresado exitosamente ✅")
            return redirect('repuestos:listar_repuestos')
    else:
        form = RepuestoForm()
    return render(request, 'registrar_repuesto.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def listar_repuestos(request):
    repuestos = Repuesto.objects.all()
    return render(request, 'listar_repuestos.html', {'repuestos': repuestos})