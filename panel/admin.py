from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils import timezone

from .models import RegistroActividad

User = get_user_model()

class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('accion', 'content_object', 'content_type', 'object_id', 'actor', 'timestamp')
    list_filter = ('content_type', 'timestamp')
    search_fields = ('accion', 'actor__username', 'object_id')
    readonly_fields = ('actor', 'accion', 'content_type', 'object_id', 'content_object', 'timestamp')
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class ActivityLogMixin:
    """
    Mixin para registrar actividades en el admin
    """
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if change:
            # Actualización
            accion = f"{obj._meta.verbose_name} actualizado: {str(obj)}"
            action_flag = CHANGE
        else:
            # Creación
            accion = f"{obj._meta.verbose_name} creado: {str(obj)}"
            action_flag = ADDITION
            
        RegistroActividad.objects.create(
            actor=request.user,
            accion=accion,
            content_object=obj
        )
        
        # Registrar en el log de Django
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=action_flag,
            change_message=''
        )

    def delete_model(self, request, obj):
        # Registrar antes de eliminar
        RegistroActividad.objects.create(
            actor=request.user,
            accion=f"{obj._meta.verbose_name} eliminado: {str(obj)}",
            content_object=obj
        )
        
        # Registrar en el log de Django
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=DELETION,
            change_message=''
        )
        
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        # Registrar eliminación múltiple
        for obj in queryset:
            RegistroActividad.objects.create(
                actor=request.user,
                accion=f"{obj._meta.verbose_name} eliminado: {str(obj)}",
                content_object=obj
            )
            
            # Registrar en el log de Django
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(obj).pk,
                object_id=obj.pk,
                object_repr=str(obj),
                action_flag=DELETION,
                change_message=''
            )
        
        super().delete_queryset(request, queryset)

# Registrar el modelo de actividades
admin.site.register(RegistroActividad, ActivityLogAdmin)
