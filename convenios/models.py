# convenios/models.py
from django.db import models
from django.conf import settings

class Convenio(models.Model):
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    CATEGORIA_CHOICES = [('Hospedaje', 'Hospedaje'), ('Salud', 'Salud'), ('Gastronomía', 'Gastronomía')]

    nombre_empresa = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    sitio_web = models.URLField(blank=True)
    imagen = models.ImageField(upload_to='convenios/', null=True, blank=True, verbose_name="Imagen del Convenio")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre_empresa

class Beneficio(models.Model):
    TIPO_CHOICES = [('Descuento', 'Descuento'), ('Servicio', 'Servicio')]
    
    nombre = models.CharField(max_length=255)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='beneficios')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.convenio.nombre_empresa})"