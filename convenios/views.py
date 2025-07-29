# convenios/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Convenio

class ConvenioListView(ListView):
    model = Convenio
    template_name = 'convenios/convenio_list.html'
    context_object_name = 'convenios'
    paginate_by = 12

    def get_queryset(self):
        return Convenio.objects.filter(estado='Activo').order_by('nombre_empresa')

class ConvenioDetailView(DetailView):
    model = Convenio
    template_name = 'convenios/convenio_detail.html'
    context_object_name = 'convenio'

    def get_queryset(self):
        return Convenio.objects.filter(estado='Activo')

class ConveniosPorCategoriaView(ListView):
    model = Convenio
    template_name = 'convenios/convenios_por_categoria.html'
    context_object_name = 'convenios'
    paginate_by = 12

    def get_queryset(self):
        categoria = self.kwargs['categoria']
        return Convenio.objects.filter(estado='Activo', categoria=categoria).order_by('nombre_empresa')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_actual'] = self.kwargs['categoria']
        context['categorias'] = Convenio.CATEGORIA_CHOICES
        return context
