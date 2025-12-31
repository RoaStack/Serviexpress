from django.urls import path
from . import views

app_name = 'boletas'

urlpatterns = [
    path('<int:pk>/', views.detalle_boleta, name='detalle_boleta'),
]
