from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from panel.admin import ActivityLogMixin
from .models import Convenio, Beneficio

@admin.register(Convenio)
class ConvenioAdmin(ActivityLogMixin, admin.ModelAdmin):
    list_display = ('nombre_empresa', 'get_categoria_display', 'estado', 'fecha_inicio', 'fecha_vencimiento')
    list_filter = ('categoria', 'estado', 'fecha_inicio')
    search_fields = ('nombre_empresa', 'descripcion')
    date_hierarchy = 'fecha_inicio'
    readonly_fields = ('created_by',)
    
    fieldsets = (
        (None, {
            'fields': ('nombre_empresa', 'categoria', 'descripcion', 'estado')
        }),
        (_('Fechas'), {
            'fields': ('fecha_inicio', 'fecha_vencimiento')
        }),
        (_('Información Adicional'), {
            'fields': ('sitio_web', 'created_by')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Beneficio)
class BeneficioAdmin(ActivityLogMixin, admin.ModelAdmin):
    list_display = ('nombre', 'get_tipo_display', 'convenio', 'activo')
    list_filter = ('tipo', 'activo')
    search_fields = ('nombre', 'descripcion', 'convenio__nombre_empresa')
    raw_id_fields = ('convenio',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['convenio'].label_from_instance = lambda obj: f"{obj.nombre_empresa} ({obj.get_categoria_display()})"
        return form
