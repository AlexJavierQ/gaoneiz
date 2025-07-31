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
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas_adicionales = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.usuario.get_full_name()} en {self.lugar.nombre}"

    def get_absolute_url(self):
        return reverse('reservas:reserva_detail', kwargs={'pk': self.pk})