# afiliaciones/views.py
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import SolicitudAfiliacion

class SolicitarAfiliacionView(LoginRequiredMixin, CreateView):
    model = SolicitudAfiliacion
    template_name = 'afiliaciones/solicitar_afiliacion.html'
    fields = ['razon_social', 'ruc', 'direccion']
    success_url = reverse_lazy('afiliaciones:solicitud_exito')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Verificar que el usuario no tenga ya una solicitud o sea socio
        if hasattr(request.user, 'solicitudafiliacion') or request.user.es_socio:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class MiSolicitudView(LoginRequiredMixin, DetailView):
    model = SolicitudAfiliacion
    template_name = 'afiliaciones/mi_solicitud.html'
    context_object_name = 'solicitud'

    def get_object(self):
        return get_object_or_404(SolicitudAfiliacion, usuario=self.request.user)

class SolicitudExitoView(LoginRequiredMixin, TemplateView):
    template_name = 'afiliaciones/solicitud_exito.html'
