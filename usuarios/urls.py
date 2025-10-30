from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import login_usuario, registro_usuario  # tus otras vistas

urlpatterns = [
    path('login/', login_usuario, name='login_usuario'),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('logout/', LogoutView.as_view(next_page='login_usuario'), name='logout_usuario'),
]
