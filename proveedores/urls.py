from django.urls import path
from . import views

app_name = "proveedores"

urlpatterns = [
    path("", views.proveedores_index, name="ficha_proveedores"),
    path("nuevo/", views.proveedor_crear, name="proveedor_crear"),
    path("<int:pk>/editar/", views.proveedor_editar, name="proveedor_editar"),
    path("<int:pk>/eliminar/", views.proveedor_eliminar, name="proveedor_eliminar"),
]
