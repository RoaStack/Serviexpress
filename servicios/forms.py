# servicios/forms.py
from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'duracion_estimada']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del servicio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'duracion_estimada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
