from django.db import models
from repuestos.models import Repuesto
from django.contrib.auth.models import User

# Create your models here.
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carrito')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'repuesto')  # Evita duplicados del mismo repuesto

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.descripcion}"

    @property
    def subtotal(self):
        return self.repuesto.precio_venta * self.cantidad
    
class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"Compra #{self.id} - {self.usuario.username}"

    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())


class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='items')
    repuesto = models.ForeignKey(Repuesto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.descripcion}"