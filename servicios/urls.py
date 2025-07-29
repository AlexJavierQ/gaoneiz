# servicios/urls.py
from django.urls import path
from . import views

app_name = 'servicios'

urlpatterns = [
    path('', views.ServicioListView.as_view(), name='servicio_list'),
    path('<int:pk>/', views.ServicioDetailView.as_view(), name='servicio_detail'),
    path('categoria/<str:categoria>/', views.ServiciosPorCategoriaView.as_view(), name='servicios_por_categoria'),
]