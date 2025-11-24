from django.db import models
from proveedores.models import Proveedor
from repuestos.models import Repuesto
from usuarios.models import Usuario

class OrdenPedido(models.Model):
    fecha = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='ordenes_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre}"

    @property
    def monto_total(self):
        return sum(det.subtotal() for det in self.detalles.all())


class DetalleOrden(models.Model):
    orden = models.ForeignKey(OrdenPedido, on_delete=models.CASCADE, related_name='detalles')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.descripcion}"

