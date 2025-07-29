# noticias/models.py

from django.db import models
from app_camara_comercio.models import Administrador # <-- Importación necesaria

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    contenido = models.TextField()
    imagen = models.ImageField(upload_to='noticias', blank=True, null=True)
    categoria = models.CharField(max_length=100)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, related_name='noticias')
    publicada = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo