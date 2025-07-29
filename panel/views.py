# panel/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import StaffRequiredMixin

class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'panel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dashboard Principal"
        # Aquí añadiremos los KPIs y datos para gráficos más adelante
        return context