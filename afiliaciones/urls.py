# afiliaciones/urls.py
from django.urls import path
from . import views

app_name = 'afiliaciones'

urlpatterns = [
    path('solicitar/', views.SolicitarAfiliacionView.as_view(), name='solicitar_afiliacion'),
    path('mi-solicitud/', views.MiSolicitudView.as_view(), name='mi_solicitud'),
    path('exito/', views.SolicitudExitoView.as_view(), name='solicitud_exito'),
]