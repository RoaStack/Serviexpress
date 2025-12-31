from django.urls import path
from . import views

app_name = "repuestos"

urlpatterns = [
    path("", views.repuestos_index, name="ficha_repuestos"),
    path("nuevo/", views.repuesto_crear, name="repuesto_crear"),
    path("<int:pk>/editar/", views.repuesto_editar, name="repuesto_editar"),
    path("<int:pk>/eliminar/", views.repuesto_eliminar, name="repuesto_eliminar"),
]
