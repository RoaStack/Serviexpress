from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "rut", "telefono", "correo", "direccion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Repuestos Don Pedro Ltda."}),
            "rut": forms.TextInput(attrs={"class": "form-control", "placeholder": "12.345.678-9"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "+56 9 1234 5678"}),
            "correo": forms.EmailInput(attrs={"class": "form-control", "placeholder": "correo@empresa.cl"}),
            "direccion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Av. Los Talleres 1234, Maipú"}),
        }