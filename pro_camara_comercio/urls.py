# pro_camera_comercio/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Rutas de Administración
    path('admin/', admin.site.urls),
    path('panel/', include('panel.urls')),
    
    # 2. Rutas de Autenticación (manejadas por django-allauth)
    path('accounts/', include('allauth.urls')),

    # 3. Rutas de Aplicaciones Específicas
    # Se delega el manejo de las URLs de cada app a su propio archivo urls.py
    path('noticias/', include('noticias.urls')),
    path('convenios/', include('convenios.urls')),
    path('servicios/', include('servicios.urls')),
    path('afiliaciones/', include('afiliaciones.urls')),
    
    # 4. Rutas de la App de Usuarios (perfil, etc.)
    # Se usa un prefijo para evitar conflictos, ej: /usuario/perfil/
    path('usuario/', include('usuarios.urls')),

    # 5. Ruta Principal (Landing Page) - DEBE IR AL FINAL
    # La app 'web' maneja la página de inicio, nosotros, contacto, etc.
    path('', include('web.urls')),
]

# 6. Configuración para servir archivos MEDIA y STATIC en modo DEBUG
# Esto es crucial para que las imágenes y CSS se puedan ver en desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)