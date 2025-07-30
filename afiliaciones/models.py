# afiliaciones/models.py
from django.db import models
from django.conf import settings

class SolicitudAfiliacion(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]

    # --- Relación con el usuario ---
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # --- Datos del Negocio ---
    razon_social = models.CharField(max_length=200)
    nombre_comercial = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13)
    ciudad = models.CharField(max_length=100)
    estado_provincia = models.CharField(max_length=100)
    tipo_negocio = models.CharField(max_length=100)

    # --- Información Comercial ---
    direccion_comercial = models.TextField(blank=True, null=True)
    tipo_actividad = models.CharField(max_length=100)
    red_social_preferida = models.CharField(max_length=100, blank=True, null=True)

    # --- Titular y Beneficiario ---
    titular_nombre = models.CharField(max_length=200)
    titular_cedula = models.CharField(max_length=10)
    titular_telefono = models.CharField(max_length=20)
    beneficiario_nombre = models.CharField(max_length=200, blank=True, null=True)
    beneficiario_pct = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # --- Archivos Adjuntos ---
    copia_cedula = models.FileField(upload_to='afiliaciones/', blank=True, null=True)
    copia_ruc = models.FileField(upload_to='afiliaciones/', blank=True, null=True)
    firma_electronica = models.FileField(upload_to='afiliaciones/', blank=True, null=True)
    documento_adicional = models.FileField(upload_to='afiliaciones/', blank=True, null=True)

    # --- Gestión Interna ---
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
