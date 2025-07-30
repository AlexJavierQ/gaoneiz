# panel/urls.py
from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    # 1. Dashboard Principal
    path('', views.DashboardView.as_view(), name='dashboard'),

    # 2. Gestión de Afiliaciones
    path('solicitudes/', views.SolicitudesAfiliacionView.as_view(), name='solicitudes_afiliacion'),
    path('solicitudes/<int:pk>/aprobar/', views.AprobarSolicitudView.as_view(), name='aprobar_solicitud'),
    path('solicitudes/<int:pk>/rechazar/', views.RechazarSolicitudView.as_view(), name='rechazar_solicitud'),
    path('solicitudes/<int:pk>/revisar/', views.SolicitudAfiliacionDetailView.as_view(), name='solicitud_revisar'),

    # 3. Gestión de Socios
    path('socios/', views.GestionSociosView.as_view(), name='gestion_socios'),
    path('socios/<int:pk>/editar/', views.SocioUpdateView.as_view(), name='socio_update'),
    path('socios/<int:pk>/eliminar/', views.SocioDeleteView.as_view(), name='socio_delete'),

    # 4. Gestión de Convenios
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('convenios/nuevo/', views.ConvenioCreateView.as_view(), name='convenio_create'),
    path('convenios/<int:pk>/editar/', views.ConvenioUpdateView.as_view(), name='convenio_update'),
    path('convenios/<int:pk>/eliminar/', views.ConvenioDeleteView.as_view(), name='convenio_delete'),

    # 5. Gestión de Noticias
    path('noticias/', views.NoticiaPanelListView.as_view(), name='noticia_panel_list'),
    path('noticias/nueva/', views.NoticiaCreateView.as_view(), name='noticia_create'),
    path('noticias/<int:pk>/editar/', views.NoticiaUpdateView.as_view(), name='noticia_update'),
    path('noticias/<int:pk>/eliminar/', views.NoticiaDeleteView.as_view(), name='noticia_delete'),

    # 6. Gestión de Servicios
    path('servicios/', views.ServicioPanelListView.as_view(), name='servicio_panel_list'),
    path('servicios/nuevo/', views.ServicioCreateView.as_view(), name='servicio_create'),
    path('servicios/<int:pk>/editar/', views.ServicioUpdateView.as_view(), name='servicio_update'),
    path('servicios/<int:pk>/eliminar/', views.ServicioDeleteView.as_view(), name='servicio_delete'),
    
    # 7. Sistema
    path('actividad/', views.RegistroActividadView.as_view(), name='registro_actividad'),

    path('reservas/', views.ReservaPanelListView.as_view(), name='reserva_panel_list'),
    path('reservas/<int:pk>/editar/', views.ReservaPanelUpdateView.as_view(), name='reserva_update'),
    
    path('lugares/', views.LugarListView.as_view(), name='lugar_list'),
    path('lugares/nuevo/', views.LugarCreateView.as_view(), name='lugar_create'),
    path('lugares/<int:pk>/editar/', views.LugarUpdateView.as_view(), name='lugar_update'),
    
    path('tipos-lugar/', views.TipoLugarListView.as_view(), name='tipo_lugar_list'),
    path('tipos-lugar/nuevo/', views.TipoLugarCreateView.as_view(), name='tipo_lugar_create'),
    path('tipos-lugar/<int:pk>/editar/', views.TipoLugarUpdateView.as_view(), name='tipo_lugar_update'),
    
]