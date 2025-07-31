from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from panel.admin import ActivityLogMixin
from .models import PerfilSocio, Usuario

User = get_user_model()

@admin.register(Usuario)
class UserAdmin(ActivityLogMixin, BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name')}),
        (_('Permisos'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

@admin.register(PerfilSocio)
class PerfilSocioAdmin(ActivityLogMixin, admin.ModelAdmin):
    list_display = ('usuario', 'razon_social', 'ruc', 'get_telefono', 'direccion', 'is_active')
    search_fields = ('usuario__email', 'razon_social', 'ruc', 'usuario__telefono')
    list_filter = ('is_active', 'tipo_plan')
    raw_id_fields = ('usuario',)
    
    def get_telefono(self, obj):
        return obj.usuario.telefono
    get_telefono.short_description = 'Teléfono'
    get_telefono.admin_order_field = 'usuario__telefono'
