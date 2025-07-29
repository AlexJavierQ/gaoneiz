# web/urls.py
from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('nosotros/', views.NosotrosView.as_view(), name='nosotros'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('contacto/exito/', views.ContactoExitoView.as_view(), name='contacto_exito'),
]