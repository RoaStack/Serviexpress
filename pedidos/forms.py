from django import forms
from .models import OrdenPedido, DetalleOrden
from proveedores.models import Proveedor
from usuarios.models import Usuario
from repuestos.models import Repuesto

class OrdenPedidoForm(forms.ModelForm):
    class Meta:
        model = OrdenPedido
<<<<<<< HEAD
        fields = ['proveedor']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'})
=======
        fields = ['proveedor', 'mecanico']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'mecanico': forms.Select(attrs={'class': 'form-control'}),
>>>>>>> staging
        }


class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = ['repuesto', 'cantidad', 'precio_unitario']
        widgets = {
            'repuesto': forms.Select(attrs={'class': 'form-control repuesto-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control cantidad-input'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-input'}),
        }
