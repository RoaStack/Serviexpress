from django.urls import path
from .views import (
    login_usuario,
    registro_cliente,
    logout_usuario,
    dashboard,
    editar_perfil
)
from django.contrib.auth.views import LogoutView

app_name = "usuarios"

urlpatterns = [
    path("login/", login_usuario, name="login_usuario"),
    path("registro/", registro_cliente, name="registro_usuario"),
    path("logout/", LogoutView.as_view(next_page="usuarios:login_usuario"), name="logout_usuario"),
    path("dashboard/", dashboard, name="dashboard"),
    path("cliente/editar/", editar_perfil, name="editar_perfil"),
]
