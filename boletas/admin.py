from django.contrib import admin
from .models import Boleta, DetalleBoleta, DetalleServicioBoleta

class DetalleBoletaInline(admin.TabularInline):
    model = DetalleBoleta
    extra = 1

class DetalleServicioBoletaInline(admin.TabularInline):
    model = DetalleServicioBoleta
    extra = 1

@admin.register(Boleta)
class BoletaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'monto_total')
    inlines = [DetalleBoletaInline, DetalleServicioBoletaInline]
