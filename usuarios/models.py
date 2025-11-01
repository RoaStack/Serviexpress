from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('MECANICO', 'Mecánico'),
        ('CLIENTE', 'Cliente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO)

    # Campos adicionales
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    comuna = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.get_tipo_usuario_display()})"

@receiver(post_save, sender=Usuario)
def asignar_grupo_automatico(sender, instance, created, **kwargs):
    if not instance.user:
        return

    grupos_por_tipo = {
        'ADMIN': 'Administradores',
        'MECANICO': 'Mecanicos',
        'CLIENTE': 'Clientes',
    }

    tipo = instance.tipo_usuario.upper()
    nombre_grupo = grupos_por_tipo.get(tipo)

    if nombre_grupo:
        grupo, _ = Group.objects.get_or_create(name=nombre_grupo)

        # Evita limpiar y reasignar si ya está en el grupo correcto
        if not instance.user.groups.filter(name=nombre_grupo).exists():
            instance.user.groups.clear()
            instance.user.groups.add(grupo)
