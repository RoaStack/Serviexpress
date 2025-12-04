from django.urls import path
from . import views

app_name = "proveedores"

urlpatterns = [
    path("", views.proveedores_index, name="ficha_proveedores"),          # Lista de proveedores
    path("crear/", views.proveedor_crear, name="crear"),                 # Crear proveedor
    path("<int:pk>/editar/", views.proveedor_editar, name="editar"),     # Editar proveedor
    path("<int:pk>/eliminar/", views.proveedor_eliminar, name="eliminar") # Eliminar proveedor
]
