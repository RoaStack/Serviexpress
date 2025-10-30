from django.db import models
from usuarios.models import Usuario
from servicios.models import Servicio

class Reserva(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_cliente')
    mecanico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='reservas_mecanico')
    servicios = models.ManyToManyField(Servicio, related_name='reservas')
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    marca_auto = models.CharField(max_length=50)
    modelo_auto = models.CharField(max_length=50)
    anio = models.IntegerField()
    estado = models.CharField(max_length=20, default='pendiente')  # pendiente, en_proceso, finalizada

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.user.username}"
