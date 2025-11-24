from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('crear/', views.crear_orden, name='crear'),
    path('precio-repuesto/<int:repuesto_id>/', views.obtener_precio_repuesto, name='precio_repuesto'),
]

