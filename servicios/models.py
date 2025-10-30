from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.PositiveIntegerField()
    duracion_estimada = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.nombre
