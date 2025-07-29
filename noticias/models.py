# noticias/models.py
from django.db import models
from django.conf import settings

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    # El autor debe ser un usuario del sistema (probablemente un staff).
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='noticias_publicadas')
    publicada = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo