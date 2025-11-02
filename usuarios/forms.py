from django import forms
from django.contrib.auth.models import User
from .models import Usuario

class RegistroClienteForm(forms.ModelForm):
    # Campos del User
    username   = forms.CharField(label="Nombre de usuario", max_length=150)
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name  = forms.CharField(label="Apellido", max_length=150)
    email      = forms.EmailField(label="Correo electrónico", required=True)
    password   = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["rut", "direccion", "comuna", "telefono"]

    # Validación amigable de username ya existente
    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso. Por favor elige otro.")
        return username

    def save(self, commit=True):
        # 1) Crear User
        user = User(
            username=self.cleaned_data["username"].strip(),
            first_name=self.cleaned_data["first_name"].strip(),
            last_name=self.cleaned_data["last_name"].strip(),
            email=self.cleaned_data["email"].strip(),
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        # 2) Crear Perfil (Usuario)
        perfil = super().save(commit=False)
        perfil.user = user
        if commit:
            perfil.save()

        # 3) Devolver el user (para login en la vista)
        return user
