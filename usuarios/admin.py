from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'telefono', 'comuna')
    list_filter = ('tipo_usuario',)
    search_fields = ('user__username', 'user__email')
