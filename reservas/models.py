# reservas/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse

class TipoLugar(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    capacidad_maxima = models.PositiveIntegerField(default=0)
    precio_por_hora = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Lugar(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoLugar, on_delete=models.PROTECT, related_name='lugares')
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='lugares/', null=True, blank=True, verbose_name="Imagen del Lugar")
    activo = models.BooleanField(default=True, help_text="Marcar para que este lugar sea visible al público.")


    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    proposito = models.CharField('Propósito', max_length=255, help_text='Propósito de la reserva', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas_adicionales = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.get_full_name()} en {self.lugar.nombre}"

    @property
    def duracion_horas(self):
        """Calcula la duración de la reserva en horas."""
        if not self.fecha_inicio or not self.fecha_fin:
            return 0
        duracion = self.fecha_fin - self.fecha_inicio
        return duracion.total_seconds() / 3600  # Convertir segundos a horas

    @property
    def costo_total(self):
        """Calcula el costo total de la reserva basado en la duración y el precio por hora del lugar."""
        if not hasattr(self, 'lugar') or not self.lugar or not hasattr(self.lugar, 'tipo') or not self.lugar.tipo:
            return 0
        from decimal import Decimal
        duration_decimal = Decimal(str(self.duracion_horas))  # Convert float to Decimal safely
        return (duration_decimal * self.lugar.tipo.precio_por_hora).quantize(Decimal('0.00'))

    def get_absolute_url(self):
        return reverse('reservas:reserva_detail', kwargs={'pk': self.pk})