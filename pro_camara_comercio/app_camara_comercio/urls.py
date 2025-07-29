# app_camara_comercio/urls.py

from django.urls import path
from . import views
from .views import NosotrosView, crear_socio
from django.urls import include

app_name = 'app_camara_comercio'

urlpatterns = [
    # --- Rutas Públicas ---
    path('', views.HomePageView.as_view(), name='home'),
    path('noticias/', include('noticias.urls')),
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('afiliacion/', views.AfiliadoCreateView.as_view(), name='afiliacion'),
    path('contacto/', views.ContactoCreateView.as_view(), name='contacto'),
    path('servicios/', views.ServicioListView.as_view(), name='servicio_list'),
    path('nosotros/', NosotrosView.as_view(), name='nosotros'),
    path('crear-socio/', crear_socio, name='crear_socio'),
    
    # --- Rutas del Dashboard (Protegidas) ---
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/perfil/', views.PerfilUpdateView.as_view(), name='perfil'),
]

# NOTA: Las URLs de login y logout ahora son manejadas por allauth
# a través del archivo urls.py principal del proyecto.