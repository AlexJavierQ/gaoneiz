# panel/urls.py

from django.urls import path
from . import views  # Importamos las vistas que hemos creado

app_name = 'panel'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('solicitudes/', views.SolicitudesAfiliacionView.as_view(), name='solicitudes_afiliacion'),
    path('solicitudes/<int:pk>/aprobar/', views.AprobarSolicitudView.as_view(), name='aprobar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', views.RechazarSolicitudView.as_view(), name='rechazar_solicitud'),
    path('socios/', views.GestionSociosView.as_view(), name='gestion_socios'),
    path('actividad/', views.RegistroActividadView.as_view(), name='registro_actividad'),
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('convenios/nuevo/', views.ConvenioCreateView.as_view(), name='convenio_create'),
    path('convenios/<int:pk>/editar/', views.ConvenioUpdateView.as_view(), name='convenio_update'),
    path('convenios/<int:pk>/eliminar/', views.ConvenioDeleteView.as_view(), name='convenio_delete'),
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('noticias/', views.NoticiaListView.as_view(), name='noticia_list'),
    path('servicios/', views.ServicioListView.as_view(), name='servicio_list'),
    path('socios/<int:pk>/editar/', views.SocioUpdateView.as_view(), name='socio_update'),
    path('socios/<int:pk>/eliminar/', views.SocioDeleteView.as_view(), name='socio_delete'),

]