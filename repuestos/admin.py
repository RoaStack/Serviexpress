from django.contrib import admin
from .models import Repuesto

@admin.register(Repuesto)
class RepuestoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'marca', 'precio_venta', 'stock', 'limite_stock')
    list_filter = ('marca',)
    search_fields = ('descripcion',)
