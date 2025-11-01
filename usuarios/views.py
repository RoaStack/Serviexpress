from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm  # ✅ Importamos el formulario

# 🧩 Registro de usuarios (ahora usando el formulario)
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # ✅ El form ya crea el User, Usuario y asigna grupo
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('login_usuario')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroUsuarioForm()  # Render inicial vacío

    return render(request, 'usuarios/registro.html', {'form': form})


# 🔐 Login
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
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Datos inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


# 🚪 Logout
@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login_usuario')
