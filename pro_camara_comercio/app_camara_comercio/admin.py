# app_camara_comercio/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Persona, Administrador, Afiliado, DocumentosAfiliado,
    Convenio, Beneficio, ServicioEspecifico, Solicitud, Contacto, Reporte
)

# --- INLINE PARA DOCUMENTOS ---
# Esta es la mejor forma de manejar la relación uno-a-uno
class DocumentosAfiliadoInline(admin.StackedInline):
    model = DocumentosAfiliado
    can_delete = False
    verbose_name_plural = 'Documentos Adjuntos'
    # Extra = 0 evita que se muestren formularios vacíos para añadir uno nuevo
    extra = 0
    
    fieldsets = (
        (None, {
            'fields': (
                ('titular_nombres', 'titular_telefono', 'titular_cedula'),
                ('beneficiario_nombres', 'beneficiario_porcentaje'),
                ('copia_ruc', 'copia_cedula'),
                ('copia_nombramiento', 'firma_electronica'),
                'consentimiento_datos'
            )
        }),
    )

# --- PANELES DE ADMINISTRACIÓN PERSONALIZADOS ---

@admin.register(Afiliado)
class AfiliadoAdmin(admin.ModelAdmin):
    inlines = (DocumentosAfiliadoInline,)
    list_display = ('razon_social', 'RUC', 'email', 'tipo_plan', 'is_active')
    list_filter = ('is_active', 'tipo_plan', 'ciudad')
    search_fields = ('razon_social', 'nombre_comercial', 'RUC', 'email', 'first_name', 'last_name')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Estado de Afiliación', {'fields': ('is_active', 'acepta_terminos')}),
        ('Información de Usuario (Login)', {'fields': ('first_name', 'last_name', 'email', 'cedula', 'telf')}),
        ('Datos Comerciales y de Plan', {'fields': ('tipo_plan', 'razon_social', 'nombre_comercial', 'RUC', 'direccion', 'ciudad', 'tipo_negocio')}),
        ('Información del Representante', {'fields': ('nombre_representante_legal', 'cedula_representante', 'red_social_preferida')}),
        ('Fechas (Automático)', {
            'fields': ('fecha_afiliacion', 'fecha_visita', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'fecha_afiliacion')
    # Pro Tip: Optimiza las consultas a la base de datos para la lista
    list_select_related = True

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'categoria', 'estado', 'fecha_inicio', 'fecha_vencimiento')
    list_filter = ('estado', 'categoria')
    search_fields = ('nombre_empresa', 'contacto_nombre')
    list_editable = ('estado', 'categoria')

    fieldsets = (
        ('Información Principal', {'fields': ('nombre_empresa', 'categoria', 'descripcion')}),
        ('Vigencia y Estado', {'fields': ('estado', 'fecha_inicio', 'fecha_vencimiento')}),
        ('Datos de Contacto de la Empresa', {
            'fields': ('contacto_nombre', 'contacto_telefono', 'contacto_email', 'direccion', 'sitio_web'),
            'classes': ('collapse',)
        }),
        ('Registro (Automático)', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ServicioEspecifico)
class ServicioEspecificoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'beneficio', 'activo')
    search_fields = ('nombre', 'beneficio__nombre')
    list_filter = ('activo', 'beneficio__tipo', 'beneficio__convenio__nombre_empresa') 
    autocomplete_fields = ('beneficio',)

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'servicio_especifico', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'fecha_solicitud', 'servicio_especifico__beneficio__convenio__categoria')
    search_fields = ('descripcion', 'afiliado__razon_social')
    list_editable = ('estado',)
    autocomplete_fields = ('afiliado', 'servicio_especifico')
    readonly_fields = ('fecha_solicitud', 'created_at', 'updated_at')
    
@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'convenio', 'tipo', 'activo')
    list_filter = ('activo', 'tipo', 'convenio__categoria')
    search_fields = ('nombre', 'convenio__nombre_empresa')
    list_editable = ('activo', 'tipo')
    autocomplete_fields = ('convenio',)

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'correo_electronico', 'asunto', 'fecha_envio')
    list_filter = ('asunto',)
    search_fields = ('nombre_completo', 'correo_electronico', 'mensaje')

    # Deshabilita la acción de borrado masivo para los contactos
    actions = None
    
    # Un método más explícito para hacer todos los campos de solo lectura
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an existing object
            return [f.name for f in self.model._meta.fields]
        return []

# --- REGISTRO DE MODELOS CON CONFIGURACIÓN BÁSICA ---
# Usamos el decorador @admin.register para mantener la consistencia
@admin.register(Administrador)
class AdministradorAdmin(UserAdmin):
    """ Heredamos de UserAdmin para una mejor visualización de los administradores """
    list_display = ('email', 'first_name', 'last_name', 'is_staff')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'fecha_generacion', 'administrador')