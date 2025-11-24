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





DIAS_SEMANA = [
    ('0', 'Lunes'),
    ('1', 'Martes'),
    ('2', 'Miércoles'),
    ('3', 'Jueves'),
    ('4', 'Viernes'),
    ('5', 'Sábado'),
    ('6', 'Domingo'),
]

HORAS_TRABAJO = [
    (f"{h:02d}:00", f"{h:02d}:00") for h in range(8, 19)
]


class DisponibilidadMasivaForm(forms.Form):
    mecanico = forms.ModelChoiceField(
        queryset=Usuario.objects.none(),
        label="Mecánico",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    fecha_inicio = forms.DateField(
        label="Desde",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    fecha_fin = forms.DateField(
        label="Hasta",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )
    dias_semana = forms.MultipleChoiceField(
        choices=DIAS_SEMANA,
        widget=forms.CheckboxSelectMultiple,
        label="Días de la semana"
    )

    # 👇 AQUÍ CAMBIAMOS A SELECT CON OPCIONES PREDEFINIDAS
    hora_inicio = forms.TimeField(
        label="Hora inicio",
        initial="08:00",
        widget=forms.Select(
            choices=HORAS_TRABAJO,
            attrs={"class": "form-select"}
        ),
    )
    hora_termino = forms.TimeField(
        label="Hora término",
        initial="18:00",
        widget=forms.Select(
            choices=HORAS_TRABAJO,
            attrs={"class": "form-select"}
        ),
    )
    colacion_inicio = forms.TimeField(
        label="Inicio colación",
        initial="13:00",
        widget=forms.Select(
            choices=HORAS_TRABAJO,
            attrs={"class": "form-select"}
        ),
    )
    colacion_termino = forms.TimeField(
        label="Fin colación",
        initial="14:00",
        widget=forms.Select(
            choices=HORAS_TRABAJO,
            attrs={"class": "form-select"}
        ),
    )

    duracion_bloque = forms.IntegerField(
        label="Duración del bloque (minutos)",
        min_value=5,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mecanico"].queryset = Usuario.objects.filter(
            user__groups__name="Mecanicos"
        )
