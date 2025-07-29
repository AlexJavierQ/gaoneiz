# convenios/urls.py
from django.urls import path
from . import views

app_name = 'convenios'

urlpatterns = [
    path('', views.ConvenioListView.as_view(), name='convenio_list'),
    path('<int:pk>/', views.ConvenioDetailView.as_view(), name='convenio_detail'),
    path('categoria/<str:categoria>/', views.ConveniosPorCategoriaView.as_view(), name='convenios_por_categoria'),
]