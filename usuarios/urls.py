# usuarios/urls.py

from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Ruta para el registro, que ahora usa la vista de allauth
    
    # Rutas para el perfil
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/editar/', views.EditarPerfilView.as_view(), name='editar_perfil'),
    
    # Ruta para el listado público de socios
    path('socios/', views.SociosListView.as_view(), name='socios_list'),
]