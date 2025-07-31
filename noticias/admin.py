from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from panel.admin import ActivityLogMixin
from .models import Noticia

@admin.register(Noticia)
class NoticiaAdmin(ActivityLogMixin, admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion', 'publicada')
    list_filter = ('publicada', 'fecha_publicacion', 'categoria')
    search_fields = ('titulo', 'contenido', 'resumen', 'autor__username')
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        (None, {
            'fields': ('titulo', 'resumen', 'contenido', 'imagen')
        }),
        (_('Metadatos'), {
            'fields': ('categoria', 'autor', 'fecha_publicacion', 'publicada')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.autor_id:
            obj.autor = request.user
        super().save_model(request, obj, form, change)