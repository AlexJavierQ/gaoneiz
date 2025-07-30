from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('registro/', views.CustomSignupView.as_view(), name='signup'),
    path('socios/', views.SociosListView.as_view(), name='socios_list'),
]