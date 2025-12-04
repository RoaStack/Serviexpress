from django.urls import path
from . import views
from .views import (
    login_usuario,
    registro_cliente,
    logout_usuario,
    dashboard,
    editar_perfil,
    ver_perfil
)
from django.contrib.auth.views import LogoutView

app_name = "usuarios"

urlpatterns = [
    path("login/", login_usuario, name="login_usuario"),
    path("registro/", registro_cliente, name="registro_usuario"),
    path("logout/", LogoutView.as_view(next_page="usuarios:login_usuario"), name="logout_usuario"),
    path("dashboard/", dashboard, name="dashboard"),
    path("cliente/editar/", editar_perfil, name="editar_perfil"),
    path("editar-perfil/", editar_perfil, name="editar_perfil"),
    path("perfil/", ver_perfil, name="ver_perfil"),
    path("perfil/editar/", editar_perfil, name="editar_perfil"),
    path("admin/mecanicos/", views.gestion_mecanicos, name="gestion_mecanicos"),
    path("admin/mecanicos/crear/", views.crear_mecanico, name="crear_mecanico"),
    path("admin/mecanicos/<int:usuario_id>/editar/", views.editar_mecanico, name="editar_mecanico"),
    path("admin/mecanicos/<int:usuario_id>/eliminar/", views.eliminar_mecanico, name="eliminar_mecanico"),
    path("admin/clientes/", views.gestion_clientes, name="gestion_clientes"),
    path("admin/clientes/crear/", views.crear_cliente, name="crear_cliente"),
    path("admin/clientes/<int:usuario_id>/editar/", views.editar_cliente, name="editar_cliente"),
    path("admin/clientes/<int:usuario_id>/eliminar/", views.eliminar_cliente, name="eliminar_cliente"),
    path("admin/reportes/", views.reportes, name="reportes"),
]
