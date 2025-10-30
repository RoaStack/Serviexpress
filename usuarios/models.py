from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    TIPOS = [
        ('ADMIN', 'Administrador'),
        ('MECANICO', 'Mecánico'),
        ('CLIENTE', 'Cliente'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=150, blank=True)
    comuna = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_usuario_display()})"
