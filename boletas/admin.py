from django.contrib import admin
from .models import Boleta, DetalleBoleta, DetalleServicioBoleta

class DetalleBoletaInline(admin.TabularInline):
    model = DetalleBoleta
    extra = 0

class DetalleServicioBoletaInline(admin.TabularInline):
    model = DetalleServicioBoleta
    extra = 0

@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'reserva', 'fecha', 'monto_total')
    inlines = [DetalleBoletaInline, DetalleServicioBoletaInline]
    search_fields = ('cliente__user__username',)
    ordering = ('-fecha',)

