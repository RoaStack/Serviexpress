from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
   path('',  views.servicio_list, name='servicio_list'),

]
