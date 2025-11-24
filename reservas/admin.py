from django.contrib import admin
from django import forms
from .models import Reserva, Disponibilidad
from usuarios.models import Usuario


# ============================================================
# 🔹 FORMULARIO PERSONALIZADO para Disponibilidad
# ============================================================
class DisponibilidadAdminForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Corregido: el filtro debe apuntar a user__groups
        self.fields['mecanico'].queryset = Usuario.objects.filter(user__groups__name="Mecanicos")


# ============================================================
# 🔹 ADMIN DISPONIBILIDAD
# ============================================================
# ============================================================
# 🔹 ADMIN DISPONIBILIDAD
# ============================================================
@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    form = DisponibilidadAdminForm

    list_display = (
        'mecanico',
        'fecha',
        'hora_inicio',
        'hora_termino',
        'colacion_inicio',
        'colacion_termino',
        'activo',
    )

    list_filter = (
        'fecha',
        'mecanico',
        'activo',
    )

    search_fields = (
        'mecanico__user__username',
    )

    ordering = (
        'fecha',
        'hora_inicio',
    )

    list_per_page = 20



# ============================================================
# 🔹 ADMIN RESERVA
# ============================================================
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'mecanico', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'mecanico')
    search_fields = ('cliente__user__username', 'mecanico__user__username', 'marca_auto', 'modelo_auto')
    ordering = ('-fecha', '-hora')
    list_per_page = 20
