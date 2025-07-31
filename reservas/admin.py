# reservas/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import TipoLugar, Lugar, Reserva

# Se registra TipoLugar para que sea visible en el admin
@admin.register(TipoLugar)
class TipoLugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'precio_por_hora', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    # CORREGIDO: Se usan campos que sí existen en el modelo Lugar.
    list_display = ('nombre', 'tipo', 'imagen_preview')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'tipo__nombre')

    # Función para mostrar una miniatura de la imagen.
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 5px;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Imagen'

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    # CORREGIDO: Se usan campos que sí existen en el modelo Reserva.
    list_display = ('usuario', 'lugar', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'lugar', 'fecha_inicio')
    search_fields = ('usuario__username', 'lugar__nombre')
    
    # CORREGIDO: 'fecha_creacion' es un campo válido para ser de solo lectura.
    readonly_fields = ('fecha_creacion',)
    
    # Se ordena por la fecha de creación más reciente.
    ordering = ('-fecha_creacion',)