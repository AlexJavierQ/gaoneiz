# panel/urls.py

from django.urls import path
from . import views  # Importamos las vistas que hemos creado
# from . import views # (Importaremos las vistas más adelante)

app_name = 'panel'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('solicitudes/', views.SolicitudesAfiliacionView.as_view(), name='solicitudes_afiliacion'),
    path('solicitudes/<int:pk>/aprobar/', views.AprobarSolicitudView.as_view(), name='aprobar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', views.RechazarSolicitudView.as_view(), name='rechazar_solicitud'),
    path('socios/', views.GestionSociosView.as_view(), name='gestion_socios'),
    path('actividad/', views.RegistroActividadView.as_view(), name='registro_actividad'),
]