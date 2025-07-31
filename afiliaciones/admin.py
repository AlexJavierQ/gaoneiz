from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from panel.admin import ActivityLogMixin
from .models import SolicitudAfiliacion

@admin.register(SolicitudAfiliacion)
class SolicitudAfiliacionAdmin(ActivityLogMixin, admin.ModelAdmin):
    list_display = ('razon_social', 'ruc', 'ciudad', 'estado', 'fecha_solicitud', 'revisado_por')
    list_filter = ('estado', 'tipo_negocio', 'fecha_solicitud')
    search_fields = ('razon_social', 'ruc', 'usuario__email', 'titular_nombre')
    date_hierarchy = 'fecha_solicitud'
    raw_id_fields = ('usuario', 'revisado_por')
    readonly_fields = ('fecha_solicitud',)
    
    fieldsets = (
        (_('Datos del Negocio'), {
            'fields': (
                'razon_social', 'nombre_comercial', 'ruc',
                'ciudad', 'estado_provincia', 'tipo_negocio'
            )
        }),
        (_('Información Comercial'), {
            'fields': (
                'direccion_comercial', 'tipo_actividad', 'red_social_preferenda'
            )
        }),
        (_('Titular y Beneficiario'), {
            'fields': (
                'titular_nombre', 'titular_cedula', 'titular_telefono',
                'beneficiario_nombre', 'beneficiario_pct'
            )
        }),
        (_('Documentos Adjuntos'), {
            'fields': (
                'copia_cedula', 'copia_ruc',
                'firma_electronica', 'documento_adicional'
            )
        }),
        (_('Gestión'), {
            'fields': (
                'estado', 'fecha_solicitud', 'fecha_revision', 'revisado_por'
            )
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si es una edición
            return self.readonly_fields + ('fecha_solicitud', 'usuario')
        return self.readonly_fields
