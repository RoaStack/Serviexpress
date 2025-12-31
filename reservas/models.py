from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario
from servicios.models import Servicio
from datetime import time
import holidays

class Disponibilidad(models.Model):
    mecanico = models.ForeignKey(Usuario,on_delete=models.CASCADE, related_name="disponibilidades")
    fecha = models.DateField(help_text="Selecciona la fecha exacta de disponibilidad")
    hora_inicio = models.TimeField(default=time(8, 0))
    hora_termino = models.TimeField(default=time(18, 0))
    duracion_bloque = models.IntegerField(default=30)  # minutos
    colacion_inicio = models.TimeField(default=time(13, 0))
    colacion_termino = models.TimeField(default=time(14, 0))
    activo = models.BooleanField(default=True)

    def clean(self):
        """
        Evita que se registre disponibilidad en días feriados en Chile.
        """
        feriados = holidays.Chile()  # 🇨🇱 Lista oficial de feriados chilenos
        if self.fecha in feriados:
            raise ValidationError(
                f"La fecha {self.fecha.strftime('%d/%m/%Y')} es feriado en Chile ({feriados.get(self.fecha)}). "
                "No se puede registrar disponibilidad ese día."
            )

    def __str__(self):
        return f"{self.mecanico.user.username} - {self.fecha}"



class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada'),
    ]


    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas_cliente')
    mecanico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservas_mecanico')
    servicios = models.ManyToManyField(Servicio, related_name='reservas')
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()

    # 🔹 Nuevo campo opcional: bloque horario de la reserva
    bloque_inicio = models.TimeField(null=True, blank=True)

    # 🔹 Asociación (opcional) a una disponibilidad concreta
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.SET_NULL, null=True, blank=True, related_name="reservas")


    
    marca_auto = models.CharField(max_length=50)
    modelo_auto = models.CharField(max_length=50)
    anio = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.user.username}"

    # 🔧 Método auxiliar para saber si la reserva está dentro del horario del mecánico
    def dentro_de_horario(self):
        if not self.disponibilidad:
            return False
        return (
            self.disponibilidad.hora_inicio <= self.hora < self.disponibilidad.hora_termino
            and not (self.disponibilidad.colacion_inicio <= self.hora < self.disponibilidad.colacion_termino)
        )
