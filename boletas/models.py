from django.db import models
from usuarios.models import Usuario
from reservas.models import Reserva
from repuestos.models import Repuesto
from servicios.models import Servicio

class Boleta(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Boleta #{self.id} - {self.cliente.user.username}"

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, related_name='detalles_repuestos')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.precio_unitario

class DetalleServicioBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, related_name='detalles_servicios')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    precio_servicio = models.PositiveIntegerField()

    def subtotal(self):
        return self.precio_servicio
