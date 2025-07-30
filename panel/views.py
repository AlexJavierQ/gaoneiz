

# panel/views.py

# Imports de la librería estándar de Python
import csv
from datetime import timedelta

# Imports de Django
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import (
    View, TemplateView, ListView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import models
from django.db.models import Count, Q
from django.db.models.functions import TruncDate, ExtractHour

# Imports de Modelos de otras apps
# --- CORRECCIÓN: Se elimina la importación de 'Rol' ---
from usuarios.models import Usuario, PerfilSocio
from afiliaciones.models import SolicitudAfiliacion
from convenios.models import Convenio
from noticias.models import Noticia
from servicios.models import Servicio

# Imports de la app actual ('panel')
from .models import RegistroActividad
from .forms import (
    UsuarioEditForm, PerfilSocioForm, ConvenioForm, 
    NoticiaForm, ServicioForm
)
from .mixins import StaffRequiredMixin
from .utils import (
    registrar_actividad, registrar_aprobacion_solicitud, 
    registrar_rechazo_solicitud, registrar_creacion,
    registrar_actualizacion, registrar_eliminacion
)

# ==============================================================================
# VISTA PRINCIPAL DEL PANEL
# ==============================================================================
class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard Principal"
        context["total_usuarios"] = Usuario.objects.count()
        context["total_socios"] = PerfilSocio.objects.filter(is_active=True).count()
        context["solicitudes_pendientes"] = SolicitudAfiliacion.objects.filter(estado="PENDIENTE").count()
        context["actividad_reciente"] = RegistroActividad.objects.select_related("actor")[:10]
        return context

# ==============================================================================
# VISTAS PARA AFILIACIONES
# ==============================================================================
class SolicitudesAfiliacionView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = SolicitudAfiliacion
    template_name = "panel/solicitudes_afiliacion.html"
    context_object_name = "solicitudes"
    paginate_by = 10

    def get_queryset(self):
        queryset = SolicitudAfiliacion.objects.filter(estado='PENDIENTE').select_related('usuario')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(razon_social__icontains=query) | Q(ruc__icontains=query) |
                Q(usuario__first_name__icontains=query) | Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        return context

class AprobarSolicitudView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        solicitud = get_object_or_404(SolicitudAfiliacion, pk=pk)
        if solicitud.estado == "PENDIENTE":
            PerfilSocio.objects.create(
                usuario=solicitud.usuario,
                razon_social=solicitud.razon_social,
                ruc=solicitud.ruc,
                direccion=solicitud.direccion,
                is_active=True,
            )
            solicitud.estado = "APROBADA"
            solicitud.fecha_revision = timezone.now()
            solicitud.revisado_por = request.user
            solicitud.save()
            
            # Registrar actividad
            registrar_aprobacion_solicitud(request.user, solicitud)
            
            messages.success(request, f"Solicitud de {solicitud.usuario.get_full_name()} aprobada.")
        return redirect("panel:solicitudes_afiliacion")

class RechazarSolicitudView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        solicitud = get_object_or_404(SolicitudAfiliacion, pk=pk)
        if solicitud.estado == "PENDIENTE":
            solicitud.estado = "RECHAZADA"
            solicitud.fecha_revision = timezone.now()
            solicitud.revisado_por = request.user
            solicitud.save()
            
            # Registrar actividad
            registrar_rechazo_solicitud(request.user, solicitud)
            
            messages.warning(request, f"Solicitud de {solicitud.usuario.get_full_name()} rechazada.")
        return redirect("panel:solicitudes_afiliacion")

# ==============================================================================
# VISTAS CRUD PARA GESTIÓN DE SOCIOS
# ==============================================================================
class GestionSociosView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = PerfilSocio
    template_name = "panel/gestion_socios.html"
    context_object_name = "socios"
    paginate_by = 15

    def get_queryset(self):
        queryset = PerfilSocio.objects.select_related("usuario").order_by("-fecha_afiliacion")
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(razon_social__icontains=query) | Q(ruc__icontains=query) |
                Q(usuario__first_name__icontains=query) | Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query)
            )
        return queryset

class SocioUpdateView(StaffRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = 'panel/socio_form.html'
    success_url = reverse_lazy('panel:gestion_socios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['perfil_form'] = PerfilSocioForm(self.request.POST, instance=self.object.perfil_socio)
        else:
            context['perfil_form'] = PerfilSocioForm(instance=self.object.perfil_socio)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        perfil_form = context['perfil_form']
        if form.is_valid() and perfil_form.is_valid():
            form.save()
            perfil_form.save()
            messages.success(self.request, f"Socio '{self.object.get_full_name()}' actualizado.")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class SocioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = PerfilSocio
    template_name = 'panel/socio_confirm_delete.html'
    success_url = reverse_lazy('panel:gestion_socios')

    def form_valid(self, form):
        messages.success(self.request, f"El perfil de socio para {self.object.razon_social} ha sido eliminado.")
        return super().form_valid(form)

# ==============================================================================
# VISTAS CRUD PARA CONVENIOS
# ==============================================================================
class ConvenioListView(StaffRequiredMixin, ListView):
    model = Convenio
    template_name = 'panel/convenio_list.html'
    context_object_name = 'convenios'
    paginate_by = 10

class ConvenioCreateView(StaffRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'panel/convenio_form.html'
    success_url = reverse_lazy('panel:convenio_list')

    def form_valid(self, form):
        convenio = form.save(commit=False)
        convenio.created_by = self.request.user
        convenio.save()
        
        # Registrar actividad
        registrar_creacion(self.request.user, convenio, "convenio")
        
        messages.success(self.request, "Convenio creado exitosamente.")
        return super().form_valid(form)

class ConvenioUpdateView(StaffRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'panel/convenio_form.html'
    success_url = reverse_lazy('panel:convenio_list')

    def form_valid(self, form):
        # Registrar actividad
        registrar_actualizacion(self.request.user, form.instance, "convenio")
        
        messages.success(self.request, "Convenio actualizado exitosamente.")
        return super().form_valid(form)

class ConvenioDeleteView(StaffRequiredMixin, DeleteView):
    model = Convenio
    template_name = 'panel/convenio_confirm_delete.html'
    success_url = reverse_lazy('panel:convenio_list')

    def form_valid(self, form):
        # Registrar actividad antes de eliminar
        registrar_eliminacion(self.request.user, self.object, "convenio")
        
        messages.success(self.request, "Convenio eliminado exitosamente.")
        return super().form_valid(form)

# ==============================================================================
# VISTAS CRUD PARA NOTICIAS
# ==============================================================================
class NoticiaPanelListView(StaffRequiredMixin, ListView):
    model = Noticia
    template_name = 'panel/noticia_list.html'
    context_object_name = 'noticias'
    paginate_by = 10

class NoticiaCreateView(StaffRequiredMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'panel/noticia_form.html'
    success_url = reverse_lazy('panel:noticia_panel_list')

    def form_valid(self, form):
        noticia = form.save(commit=False)
        noticia.autor = self.request.user
        noticia.save()
        messages.success(self.request, "Noticia creada exitosamente.")
        return redirect(self.success_url)

class NoticiaUpdateView(StaffRequiredMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = 'panel/noticia_form.html'
    success_url = reverse_lazy('panel:noticia_panel_list')

    def form_valid(self, form):
        messages.success(self.request, "Noticia actualizada exitosamente.")
        return super().form_valid(form)

class NoticiaDeleteView(StaffRequiredMixin, DeleteView):
    model = Noticia
    template_name = 'panel/noticia_confirm_delete.html'
    success_url = reverse_lazy('panel:noticia_panel_list')

    def form_valid(self, form):
        messages.success(self.request, f"La noticia '{self.object.titulo}' ha sido eliminada.")
        return super().form_valid(form)

# ==============================================================================
# VISTAS CRUD PARA SERVICIOS
# ==============================================================================
class ServicioPanelListView(StaffRequiredMixin, ListView):
    model = Servicio
    template_name = 'panel/servicio_list.html'
    context_object_name = 'servicios'
    paginate_by = 10

class ServicioCreateView(StaffRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'panel/servicio_form.html'
    success_url = reverse_lazy('panel:servicio_panel_list')

    def form_valid(self, form):
        messages.success(self.request, "Servicio creado exitosamente.")
        return super().form_valid(form)

class ServicioUpdateView(StaffRequiredMixin, UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'panel/servicio_form.html'
    success_url = reverse_lazy('panel:servicio_panel_list')

    def form_valid(self, form):
        messages.success(self.request, "Servicio actualizado exitosamente.")
        return super().form_valid(form)

class ServicioDeleteView(StaffRequiredMixin, DeleteView):
    model = Servicio
    template_name = 'panel/servicio_confirm_delete.html'
    success_url = reverse_lazy('panel:servicio_panel_list')

    def form_valid(self, form):
        messages.success(self.request, f"El servicio '{self.object.nombre}' ha sido eliminado.")
        return super().form_valid(form)

# ==============================================================================
# VISTAS DE SISTEMA
# ==============================================================================
class RegistroActividadView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = RegistroActividad
    template_name = "panel/registro_actividad.html"
    context_object_name = "actividades"
    paginate_by = 50

    def get_queryset(self):
        queryset = RegistroActividad.objects.select_related("actor", "content_type").order_by("-timestamp")
        
        # Filtro de búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(accion__icontains=query) |
                Q(actor__first_name__icontains=query) |
                Q(actor__last_name__icontains=query) |
                Q(actor__email__icontains=query)
            )
        
        # Filtro por tipo de contenido
        content_type = self.request.GET.get('tipo')
        if content_type:
            queryset = queryset.filter(content_type__model=content_type)
        
        # Filtro por fecha
        fecha = self.request.GET.get('fecha')
        if fecha:
            try:
                from datetime import datetime
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                queryset = queryset.filter(timestamp__date=fecha_obj)
            except ValueError:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        context['current_tipo'] = self.request.GET.get('tipo', '')
        context['current_fecha'] = self.request.GET.get('fecha', '')
        
        # Estadísticas adicionales
        from django.utils import timezone
        today = timezone.now().date()
        context['actividades_hoy'] = RegistroActividad.objects.filter(timestamp__date=today).count()
        
        return context
