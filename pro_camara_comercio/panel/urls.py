# panel/urls.py

from django.urls import path
from . import views  # Importamos las vistas que hemos creado
# from . import views # (Importaremos las vistas más adelante)

app_name = 'panel'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
]