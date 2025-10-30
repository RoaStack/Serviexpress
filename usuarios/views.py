# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Usuario

# Registro de usuarios
def registro_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        tipo_usuario = request.POST['tipo_usuario']

        # Crear el usuario base de Django
        user = User.objects.create_user(username=username, email=email, password=password)
        usuario = Usuario.objects.create(user=user, tipo_usuario=tipo_usuario)

        # Asignar grupo según tipo de usuario
        grupo = Group.objects.get(name=tipo_usuario.capitalize() + 's')  # Ej: Clientes, Mecanicos
        user.groups.add(grupo)

        messages.success(request, f'Usuario {username} registrado correctamente')
        return redirect('login_usuario')

    return render(request, 'usuarios/registro.html')

# Login
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenido {user.username}')
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Datos inválidos')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

# Logout
@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login_usuario')
