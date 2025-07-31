# panel/utils.py
from django.contrib.contenttypes.models import ContentType
from .models import RegistroActividad

def registrar_actividad(actor, accion, content_object=None):
    """
    Registra una actividad en el sistema solo si el usuario es administrador.
    
    Args:
        actor: Usuario que realiza la acción
        accion: Descripción de la acción realizada
        content_object: Objeto relacionado con la acción (opcional)
    """
    # Solo registrar actividades de usuarios administradores (staff)
    if not actor or not actor.is_staff:
        return None
    
    actividad = RegistroActividad(
        actor=actor,
        accion=accion
    )
    
    if content_object:
        actividad.content_type = ContentType.objects.get_for_model(content_object)
        actividad.object_id = content_object.pk
    
    try:
        actividad.save()
        return actividad
    except Exception as e:
        # En caso de error, podríamos loggear aquí
        return None

# Funciones específicas para diferentes tipos de actividades
def registrar_login(usuario):
    """Registra cuando un usuario inicia sesión"""
    return registrar_actividad(usuario, f"Inició sesión en el sistema")

def registrar_logout(usuario):
    """Registra cuando un usuario cierra sesión"""
    return registrar_actividad(usuario, f"Cerró sesión del sistema")

def registrar_creacion(usuario, objeto, tipo_objeto):
    """Registra la creación de un objeto"""
    return registrar_actividad(
        usuario, 
        f"Creó {tipo_objeto}: {str(objeto)}", 
        objeto
    )

def registrar_actualizacion(usuario, objeto, tipo_objeto):
    """Registra la actualización de un objeto"""
    return registrar_actividad(
        usuario, 
        f"Actualizó {tipo_objeto}: {str(objeto)}", 
        objeto
    )

def registrar_eliminacion(usuario, objeto, tipo_objeto):
    """Registra la eliminación de un objeto"""
    # Verificar que el usuario sea staff
    if not usuario or not usuario.is_staff:
        return None
    
    # Crear descripción más detallada
    descripcion = f"Eliminó {tipo_objeto}: {str(objeto)}"
    
    return registrar_actividad(usuario, descripcion, objeto)

def registrar_aprobacion_solicitud(usuario, solicitud):
    """Registra la aprobación de una solicitud"""
    return registrar_actividad(
        usuario,
        f"Aprobó solicitud de afiliación de {solicitud.usuario.get_full_name()}",
        solicitud
    )

def registrar_rechazo_solicitud(usuario, solicitud):
    """Registra el rechazo de una solicitud"""
    return registrar_actividad(
        usuario,
        f"Rechazó solicitud de afiliación de {solicitud.usuario.get_full_name()}",
        solicitud
    )

def registrar_nueva_solicitud(usuario, solicitud):
    """Registra una nueva solicitud de afiliación"""
    return registrar_actividad(
        usuario,
        f"Envió solicitud de afiliación para {solicitud.razon_social}",
        solicitud
    )