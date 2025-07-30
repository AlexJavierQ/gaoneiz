from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import TipoLugar, Lugar, Reserva

@admin.register(TipoLugar)
class TipoLugarAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'capacidad_maxima', 'precio_por_hora', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    list_editable = ['activo']

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'ubicacion', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'ubicacion']
    list_editable = ['activo']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = [
        'usuario', 'lugar', 'fecha_inicio', 'fecha_fin', 
        'estado_badge', 'numero_personas', 'costo_total'
    ]
    list_filter = ['estado', 'lugar__tipo', 'fecha_inicio', 'fecha_solicitud']
    search_fields = ['usuario__email', 'usuario__first_name', 'usuario__last_name', 'lugar__nombre']
    readonly_fields = ['fecha_solicitud', 'fecha_actualizacion', 'costo_total', 'duracion_horas']
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('usuario', 'lugar', 'fecha_inicio', 'fecha_fin', 'proposito', 'descripcion', 'numero_personas')
        }),
        ('Estado y Gestión', {
            'fields': ('estado', 'aprobada_por', 'fecha_aprobacion', 'notas_admin')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_solicitud', 'fecha_actualizacion', 'duracion_horas', 'costo_total'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['aprobar_reservas', 'rechazar_reservas', 'cancelar_reservas']
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': 'warning',
            'aprobada': 'success',
            'rechazada': 'danger',
            'cancelada': 'secondary',
            'completada': 'info'
        }
        color = colors.get(obj.estado, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def aprobar_reservas(self, request, queryset):
        updated = queryset.filter(estado='pendiente').update(
            estado='aprobada',
            aprobada_por=request.user,
            fecha_aprobacion=timezone.now()
        )
        self.message_user(request, f'{updated} reservas aprobadas.')
    aprobar_reservas.short_description = "Aprobar reservas seleccionadas"
    
    def rechazar_reservas(self, request, queryset):
        updated = queryset.filter(estado='pendiente').update(estado='rechazada')
        self.message_user(request, f'{updated} reservas rechazadas.')
    rechazar_reservas.short_description = "Rechazar reservas seleccionadas"
    
    def cancelar_reservas(self, request, queryset):
        updated = queryset.update(estado='cancelada')
        self.message_user(request, f'{updated} reservas canceladas.')
    cancelar_reservas.short_description = "Cancelar reservas seleccionadas"
    
    def save_model(self, request, obj, form, change):
        if change and 'estado' in form.changed_data:
            if obj.estado == 'aprobada' and not obj.aprobada_por:
                obj.aprobada_por = request.user
                obj.fecha_aprobacion = timezone.now()
        super().save_model(request, obj, form, change)