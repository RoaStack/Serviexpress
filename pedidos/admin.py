from django.contrib import admin
from .models import OrdenPedido, DetalleOrden

class DetalleOrdenInline(admin.TabularInline):
    model = DetalleOrden
    extra = 1

@admin.register(OrdenPedido)
class OrdenPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'proveedor', 'mecanico', 'fecha', 'monto_total')
    inlines = [DetalleOrdenInline]
