# pro_camera_comercio/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('panel/', include('panel.urls')),
    
    # --- ASEGÚRATE DE QUE ESTA LÍNEA EXISTA ---
    path('noticias/', include('noticias.urls')),

    # La app principal va al final
    path('', include('app_camara_comercio.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)