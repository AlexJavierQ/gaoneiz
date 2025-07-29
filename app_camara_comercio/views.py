# app_camara_comercio/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView
from django.http import Http404 # <-- LÍNEA CORREGIDA

# --- Imports de nuestro proyecto ---
from .models import (
    Convenio, 
    Afiliado, 
    Contacto, 
    Beneficio, 
    ServicioEspecifico
)
from .forms import (
    AfiliadoCreationForm, 
    ContactoForm, 
    AfiliadoUpdateForm, 
    SocioForm
)

# ==============================================================================
# VISTAS PÚBLICAS Y BASADAS EN CLASES
# ==============================================================================

class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['socios_activos'] = Afiliado.objects.filter(is_active=True).count()
        context['convenios_activos'] = Convenio.objects.filter(estado='Activo').count()
        context['beneficios_list'] = Beneficio.objects.filter(activo=True)[:3]
        return context



class ConvenioListView(ListView):
    model = Convenio
    template_name = 'convenio_list.html'
    context_object_name = 'convenios'
    
    def get_queryset(self):
        return Convenio.objects.filter(estado='Activo').order_by('categoria', 'nombre_empresa')

class AfiliadoCreateView(CreateView):
    form_class = AfiliadoCreationForm
    template_name = 'afiliacion_form.html'
    success_url = reverse_lazy('app_camara_comercio:home')

    def form_valid(self, form):
        messages.success(self.request, "¡Registro exitoso! Tu solicitud será revisada.")
        return super().form_valid(form)

class ContactoCreateView(CreateView):
    form_class = ContactoForm
    template_name = 'contacto_form.html'
    success_url = reverse_lazy('app_camara_comercio:home')

    def form_valid(self, form):
        messages.success(self.request, "¡Gracias por contactarnos!")
        return super().form_valid(form)

class ServicioListView(ListView):
    model = ServicioEspecifico
    template_name = 'servicio_list.html'
    context_object_name = 'servicios'

    def get_queryset(self):
        return ServicioEspecifico.objects.filter(activo=True).order_by('-created_at')

class NosotrosView(TemplateView):
    template_name = 'nosotros.html'

# ==============================================================================
# VISTAS DEL DASHBOARD DE USUARIO
# ==============================================================================

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['convenios'] = Convenio.objects.filter(estado='Activo')[:3]
        context['reservas_activas'] = []
        return context

class PerfilUpdateView(LoginRequiredMixin, UpdateView):
    model = Afiliado
    form_class = AfiliadoUpdateForm
    template_name = 'perfil.html'
    success_url = reverse_lazy('app_camara_comercio:dashboard')

    def get_object(self, queryset=None):
        try:
            return self.request.user.afiliado
        except Afiliado.DoesNotExist:
            raise Http404("No tienes un perfil de afiliado para editar.")

def crear_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_camara_comercio:dashboard')
    else:
        form = SocioForm()
    return render(request, 'crear_socio.html', {'form': form})