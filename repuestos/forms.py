from django import forms
from .models import Repuesto

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['foto','nombre','marca','precio_compra','precio_venta', 'stock', 'limite_stock']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del repuesto'}),
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marca del repuesto'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'limite_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
