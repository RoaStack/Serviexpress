from django.urls import path
from . import views

app_name = 'repuestos'

urlpatterns = [
    path('crear/', views.crear_repuesto, name='crear_repuesto'),
]
