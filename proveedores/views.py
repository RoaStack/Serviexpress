from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Proveedor
from .forms import ProveedorForm

def proveedores_index(request):
    proveedores = Proveedor.objects.all()
    return render(request, "proveedores/ficha_proveedores.html", {"proveedores": proveedores})


@login_required  
def proveedor_crear(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("proveedores:ficha_proveedores")  # redirige al listado
    else:
        form = ProveedorForm()
    return render(request, "proveedores/form.html", {"form": form})



