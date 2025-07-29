# afiliaciones/models.py
from django.db import models
from django.conf import settings

class SolicitudAfiliacion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    # La solicitud la hace un Usuario existente que aún no es socio.
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Datos que el usuario llena en el formulario de afiliación.
    razon_social = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13)
    direccion = models.TextField()
    # Puedes añadir más campos si el formulario de solicitud los requiere (ej. copia de cédula).
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    revisado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='solicitudes_revisadas'
    )

    def __str__(self):
        return f"Solicitud de {self.usuario.get_full_name()}"