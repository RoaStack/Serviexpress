from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('crear/', views.crear_proveedor, name='crear_proveedor'),
]
