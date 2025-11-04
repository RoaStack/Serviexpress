from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("nueva/", views.crear_reserva, name="crear_reserva"),
    path("mis_reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:pk>/", views.cancelar_reserva, name="cancelar_reserva"),
    path("cambiar_estado/<int:pk>/<str:nuevo_estado>/",views.cambiar_estado_reserva,name="cambiar_estado_reserva"),
    path("ordenes_asignadas/",views.ordenes_asignadas,name="ordenes_asignadas"),
    path("servicios_en_proceso/",views.servicios_en_proceso,name="servicios_en_proceso"),
    path("historial_servicios/",views.historial_servicios,name="historial_servicios"),
    path("actualizar_estado/<int:pk>/<str:nuevo_estado>/",views.actualizar_estado_mecanico,name="actualizar_estado_mecanico"),
]
