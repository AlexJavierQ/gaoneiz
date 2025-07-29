# usuarios/views.py
from django.views.generic import DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Usuario, PerfilSocio

class PerfilView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/perfil.html'
    context_object_name = 'usuario'

    def get_object(self):
        return self.request.user

class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'usuarios/editar_perfil.html'
    fields = ['first_name', 'last_name', 'cedula', 'telefono']
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self):
        return self.request.user

class SociosListView(ListView):
    model = PerfilSocio
    template_name = 'usuarios/socios_list.html'
    context_object_name = 'socios'
    paginate_by = 20

    def get_queryset(self):
        return PerfilSocio.objects.filter(is_active=True).select_related('usuario').order_by('razon_social')
