# web/models.py
from django.db import models

class Contacto(models.Model):
    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True)
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.nombre_completo} sobre "{self.asunto}"'