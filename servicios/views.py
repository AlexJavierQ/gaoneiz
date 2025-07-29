# servicios/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Servicio

class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicios/servicio_list.html'
    context_object_name = 'servicios'
    paginate_by = 12

    def get_queryset(self):
        queryset = Servicio.objects.filter(activo=True)
        # Si el usuario no es socio, filtrar servicios solo para socios
        if not (self.request.user.is_authenticated and self.request.user.es_socio):
            queryset = queryset.filter(solo_socios=False)
        return queryset.order_by('categoria', 'nombre')

class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'servicios/servicio_detail.html'
    context_object_name = 'servicio'

    def get_queryset(self):
        queryset = Servicio.objects.filter(activo=True)
        # Si el usuario no es socio, filtrar servicios solo para socios
        if not (self.request.user.is_authenticated and self.request.user.es_socio):
            queryset = queryset.filter(solo_socios=False)
        return queryset

class ServiciosPorCategoriaView(ListView):
    model = Servicio
    template_name = 'servicios/servicios_por_categoria.html'
    context_object_name = 'servicios'
    paginate_by = 12

    def get_queryset(self):
        categoria = self.kwargs['categoria']
        queryset = Servicio.objects.filter(activo=True, categoria=categoria)
        # Si el usuario no es socio, filtrar servicios solo para socios
        if not (self.request.user.is_authenticated and self.request.user.es_socio):
            queryset = queryset.filter(solo_socios=False)
        return queryset.order_by('nombre')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_actual'] = self.kwargs['categoria']
        context['categorias'] = Servicio.CATEGORIA_CHOICES
        return context
