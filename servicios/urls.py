from django.urls import path
from . import views

app_name = "servicios"

urlpatterns = [
    path('crear/', views.crear_servicio, name='crear_servicio'),
    path('listar/', views.listar_servicios, name='listar_servicios'),
    path('editar/<int:pk>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar/<int:pk>/', views.eliminar_servicio, name='eliminar_servicio'),
]
