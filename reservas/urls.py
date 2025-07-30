from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    path('lugares/', views.LugarListView.as_view(), name='lugares_list'),
    path('nueva/', views.ReservaCreateView.as_view(), name='nueva_reserva'),
    path('mis-reservas/', views.MisReservasView.as_view(), name='mis_reservas'),
    path('reserva/<int:pk>/', views.ReservaDetailView.as_view(), name='reserva_detail'),
    path('cancelar/<int:pk>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('verificar-disponibilidad/', views.verificar_disponibilidad, name='verificar_disponibilidad'),
]