# afiliaciones/views.py
from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import SolicitudAfiliacion
from .forms import SolicitudAfiliacionForm # <-- Importamos el nuevo formulario

class SolicitarAfiliacionView(LoginRequiredMixin, CreateView):
    model = SolicitudAfiliacion
    form_class = SolicitudAfiliacionForm # <-- Usamos el form_class
    template_name = 'afiliaciones/solicitar_afiliacion.html'
    success_url = reverse_lazy('afiliaciones:solicitud_exito')

    def form_valid(self, form):
        # Asignamos el usuario logueado a la solicitud antes de guardarla
        form.instance.usuario = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        # Evita que un socio o alguien con una solicitud ya hecha, la vuelva a solicitar
        if request.user.is_authenticated and (request.user.es_socio or hasattr(request.user, 'solicitudafiliacion')):
            return redirect(reverse_lazy('afiliaciones:mi_solicitud'))
        return super().dispatch(request, *args, **kwargs)


class MiSolicitudView(LoginRequiredMixin, DetailView):
    model = SolicitudAfiliacion
    template_name = 'afiliaciones/mi_solicitud.html'
    context_object_name = 'solicitud'

    def get_object(self, queryset=None):
        # Asegura que el usuario solo pueda ver su propia solicitud
        return SolicitudAfiliacion.objects.get(usuario=self.request.user)


class SolicitudExitoView(LoginRequiredMixin, TemplateView):
    template_name = 'afiliaciones/solicitud_exito.html'