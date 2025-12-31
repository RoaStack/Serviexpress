from django.db import models
from cloudinary.models import CloudinaryField

class Repuesto(models.Model):
    foto = CloudinaryField('foto', folder='repuestos/',null=True,blank=True)
    nombre = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    precio_compra = models.PositiveIntegerField()
    precio_venta = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    limite_stock = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.nombre

