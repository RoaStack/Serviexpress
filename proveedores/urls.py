from django.urls import path
from . import views

app_name = "proveedores"

urlpatterns = [
    path("", views.proveedores_index, name="ficha_proveedores"),
    path("crear/", views.proveedor_crear, name="crear"),
]


