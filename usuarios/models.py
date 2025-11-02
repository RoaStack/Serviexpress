from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Usuario(models.Model):
    """
    Perfil extendido para todos los usuarios del sistema (clientes, mecánicos, admins).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")

    # Campos adicionales según requerimiento
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=150)
    comuna = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuarios"
        ordering = ["user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"

    @property
    def nombre_completo(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse("usuarios:detalle", kwargs={"pk": self.pk})
