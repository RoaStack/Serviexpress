from django.urls import path
from . import views

app_name = "reservas"
app_name = "reservas"

urlpatterns = [
    path("nueva/", views.crear_reserva, name="crear_reserva"),
    path("mis_reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:pk>/", views.cancelar_reserva, name="cancelar_reserva"),
    path("cambiar_estado/<int:pk>/<str:nuevo_estado>/", views.cambiar_estado_reserva, name="cambiar_estado_reserva"),
    path("ordenes_asignadas/", views.ordenes_asignadas, name="ordenes_asignadas"),
    path("servicios_en_proceso/", views.servicios_en_proceso, name="servicios_en_proceso"),
    path("historial_servicios/", views.historial_servicios, name="historial_servicios"),
    path("actualizar_estado/<int:pk>/<str:nuevo_estado>/", views.actualizar_estado_mecanico, name="actualizar_estado_mecanico"),
    path("horas_disponibles/", views.obtener_horas_disponibles, name="horas_disponibles"),

    # 🔹 Repuestos
    path("registrar-repuestos/<int:reserva_id>/", views.registrar_repuestos_reserva, name="registrar_repuestos_reserva"),
    path("registrar-repuestos/<int:reserva_id>/eliminar/<int:detalle_id>/", views.eliminar_repuesto_detalle, name="eliminar_repuesto_detalle"),

    # 🔹 Vista del cliente: servicios finalizados
    path("servicios_realizados/", views.servicios_realizados_cliente, name="servicios_realizados_cliente"),

    # Admin genera disponibilidades masivas
    path("admin/disponibilidades/masivas/", views.crear_disponibilidades_masivas, name="crear_disponibilidades_masivas"),

]

