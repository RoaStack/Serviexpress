from django import forms
from .models import DetalleBoleta
from repuestos.models import Repuesto

class DetalleBoletaForm(forms.ModelForm):
    repuesto = forms.ModelChoiceField(
        queryset=Repuesto.objects.all(),
        label="Repuesto utilizado",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_repuesto'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        label="Cantidad",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_cantidad'})
    )
    precio_unitario = forms.IntegerField(
        required=False,
        label="Precio unitario",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_precio_unitario'})
    )

    class Meta:
        model = DetalleBoleta
        fields = ['repuesto', 'cantidad', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar stock y precio en el menú desplegable
        self.fields['repuesto'].label_from_instance = (
            lambda obj: f"{obj.descripcion} (Stock: {obj.stock}, ${obj.precio_venta})"
        )

    def clean(self):
        """
        Valida el formulario y asigna automáticamente el precio de venta.
        """
        cleaned_data = super().clean()
        repuesto = cleaned_data.get("repuesto")

        if repuesto:
            cleaned_data["precio_unitario"] = repuesto.precio_venta

        return cleaned_data

