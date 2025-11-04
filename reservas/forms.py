from django import forms
from .models import Reserva
from usuarios.models import Usuario


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["servicios", "descripcion", "fecha", "hora", "marca_auto", "modelo_auto", "anio"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 2, "placeholder": "Describe brevemente el motivo de tu reserva..."}),
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Filtra mecánicos válidos (aunque el campo no se muestre en el formulario del cliente)
        if "mecanico" in self.fields:
            self.fields["mecanico"].queryset = Usuario.objects.filter(user__groups__name="Mecanicos")

        # Opcional: Mejora visual de los campos
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
