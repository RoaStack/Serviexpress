from django import forms
from django.contrib.auth.models import User, Group
from .models import Usuario

class RegistroUsuarioForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'direccion', 'comuna', 'telefono', 'tipo_usuario']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        usuario = super().save(commit=False)
        usuario.user = user
        if commit:
            usuario.save()

        # 🔄 Asignar grupo según tipo_usuario
        grupos_por_tipo = {
            'ADMIN': 'Administradores',
            'MECANICO': 'Mecanicos',
            'CLIENTE': 'Clientes'
        }
        tipo = usuario.tipo_usuario.upper()
        nombre_grupo = grupos_por_tipo.get(tipo)
        if nombre_grupo:
            grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
            user.groups.add(grupo)
        return usuario
