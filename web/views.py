# web/views.py
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Contacto

class HomeView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí puedes agregar noticias recientes, convenios destacados, etc.
        return context

class NosotrosView(TemplateView):
    template_name = 'web/nosotros.html'

class ContactoView(CreateView):
    model = Contacto
    template_name = 'web/contacto.html'
    fields = ['nombre_completo', 'correo_electronico', 'telefono', 'asunto', 'mensaje']
    success_url = reverse_lazy('web:contacto_exito')

class ContactoExitoView(TemplateView):
    template_name = 'web/contacto_exito.html'
