from django import forms
from django.contrib.auth.models import User
from .models import Usuario


class RegistroClienteForm(forms.ModelForm):
    username   = forms.CharField(label="Nombre de usuario", max_length=150)
    first_name = forms.CharField(label="Nombre", max_length=150)
    last_name  = forms.CharField(label="Apellido", max_length=150)
    email      = forms.EmailField(label="Correo electrónico", required=True)
    password   = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ["rut", "direccion", "comuna", "telefono"]

    # APLICAR CLASES Y PLACEHOLDERS A TODOS LOS CAMPOS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "password": "Contraseña",
            "rut": "RUT",
            "direccion": "Dirección",
            "comuna": "Comuna",
            "telefono": "Teléfono",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "login-input",
                "autocomplete": "off",
                "placeholder": placeholders.get(name, "")
            })

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data["username"].strip(),
            first_name=self.cleaned_data["first_name"].strip(),
            last_name=self.cleaned_data["last_name"].strip(),
            email=self.cleaned_data["email"].strip(),
        )
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        perfil = super().save(commit=False)
        perfil.user = user
        if commit:
            perfil.save()

        return user


class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["rut", "direccion", "comuna", "telefono"]
        labels = {
            "rut": "RUT",
            "direccion": "Dirección",
            "comuna": "Comuna",
            "telefono": "Teléfono",
        }
