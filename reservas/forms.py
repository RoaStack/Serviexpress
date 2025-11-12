from django import forms
from .models import Reserva
from usuarios.models import Usuario

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["servicios", "descripcion", "fecha", "hora", "marca_auto", "modelo_auto", "anio"]
        widgets = {
            "descripcion": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Describe brevemente el motivo de tu reserva..."
            }),
            "fecha": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            # 🔹 Cambiado de TimeInput a Select (para que el JS inserte las horas disponibles)
            "hora": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Filtra mecánicos válidos (aunque el campo no se muestre en el formulario del cliente)
        if "mecanico" in self.fields:
            self.fields["mecanico"].queryset = Usuario.objects.filter(user__groups__name="Mecanicos")

        # ✅ Estilos uniformes para todos los campos
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} form-control".strip()

        # ✅ Placeholder para el select de hora
        self.fields["hora"].choices = [("", "Selecciona una hora disponible...")]
