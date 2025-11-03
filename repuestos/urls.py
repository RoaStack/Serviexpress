from django.urls import path
from . import views

app_name = 'repuestos'

urlpatterns = [
    path('crear/', views.registrar_repuesto, name='registrar_repuesto'),
    path('listar/', views.listar_repuestos, name='listar_repuestos'),
]
