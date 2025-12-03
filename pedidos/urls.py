from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('crear/', views.crear_orden, name='crear'),
    path('mis-ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('orden/<int:orden_id>/', views.detalle_orden, name='detalle_orden'),
    path('precio-repuesto/<int:repuesto_id>/', views.obtener_precio_repuesto, name='precio_repuesto'),
    path('orden/<int:orden_id>/recepcionar/', views.recepcionar_orden, name='recepcionar_orden'),

]

