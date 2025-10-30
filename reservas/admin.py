from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'mecanico', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__user__username', 'mecanico__user__username')
