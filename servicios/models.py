# servicios/models.py
from django.db import models
from django.conf import settings

class Servicio(models.Model):
    CATEGORIA_CHOICES = [
        ('CAPACITACION', 'Capacitación'),
        ('CONSULTORIA', 'Consultoría'),
        ('TRAMITES', 'Trámites'),
        ('EVENTOS', 'Eventos'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    solo_socios = models.BooleanField(default=False, help_text="Si está marcado, solo los socios pueden acceder")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
