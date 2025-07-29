# noticias/urls.py

from django.urls import path
from . import views

# --- ASEGÚRATE DE QUE ESTA LÍNEA EXISTA ---
# Esta línea crea el "namespace" que Django está buscando
app_name = 'noticias'

urlpatterns = [
    path('', views.NoticiaListView.as_view(), name='noticia_list'),
    path('<int:pk>/', views.NoticiaDetailView.as_view(), name='noticia_detail'),
]