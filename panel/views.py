# panel/views.py
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse_lazy

from .mixins import StaffRequiredMixin
from .models import RegistroActividad
from .forms import ConvenioForm

from afiliaciones.models import SolicitudAfiliacion
from usuarios.models import Usuario, PerfilSocio
from convenios.models import Convenio

from noticias.models import Noticia
from servicios.models import Servicio
from .forms import UsuarioEditForm, PerfilSocioForm

from django.db.models import Q
class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard Principal"

        # KPIs básicos
        context["total_usuarios"] = Usuario.objects.count()
        context["total_socios"] = PerfilSocio.objects.filter(is_active=True).count()
        context["solicitudes_pendientes"] = SolicitudAfiliacion.objects.filter(
            estado="PENDIENTE"
        ).count()
        context["actividad_reciente"] = RegistroActividad.objects.select_related(
            "actor"
        )[:10]

        return context


class SolicitudesAfiliacionView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = SolicitudAfiliacion
    template_name = "panel/solicitudes_afiliacion.html"
    context_object_name = "solicitudes"
    paginate_by = 10 # Opcional: para paginar la lista

    def get_queryset(self):
        # Obtenemos solo las solicitudes que están pendientes de revisión
        queryset = SolicitudAfiliacion.objects.filter(estado='PENDIENTE').select_related('usuario')
        
        # Lógica de búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(razon_social__icontains=query) |
                Q(ruc__icontains=query) |
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        # Pasamos el término de búsqueda a la plantilla para mantenerlo en la barra
        context = super().get_context_data(**kwargs)
        context['current_query'] = self.request.GET.get('q', '')
        return context


class AprobarSolicitudView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        solicitud = get_object_or_404(SolicitudAfiliacion, pk=pk)

        if solicitud.estado == "PENDIENTE":
            # Crear perfil de socio
            PerfilSocio.objects.create(
                usuario=solicitud.usuario,
                razon_social=solicitud.razon_social,
                ruc=solicitud.ruc,
                direccion=solicitud.direccion,
                tipo_plan="EMPRESA",  # Por defecto
                is_active=True,
            )

            # Actualizar solicitud
            solicitud.estado = "APROBADA"
            solicitud.fecha_revision = timezone.now()
            solicitud.revisado_por = request.user
            solicitud.save()

            messages.success(
                request,
                f"Solicitud de {solicitud.usuario.get_full_name()} aprobada exitosamente.",
            )

        return redirect("panel:solicitudes_afiliacion")


class RechazarSolicitudView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        solicitud = get_object_or_404(SolicitudAfiliacion, pk=pk)

        if solicitud.estado == "PENDIENTE":
            solicitud.estado = "RECHAZADA"
            solicitud.fecha_revision = timezone.now()
            solicitud.revisado_por = request.user
            solicitud.save()

            messages.warning(
                request, f"Solicitud de {solicitud.usuario.get_full_name()} rechazada."
            )

        return redirect("panel:solicitudes_afiliacion")


class GestionSociosView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = PerfilSocio
    template_name = "panel/gestion_socios.html"
    context_object_name = "socios"
    paginate_by = 20

    def get_queryset(self):
        return PerfilSocio.objects.select_related("usuario").order_by(
            "-fecha_afiliacion"
        )


class RegistroActividadView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = RegistroActividad
    template_name = "panel/registro_actividad.html"
    context_object_name = "actividades"
    paginate_by = 50

    def get_queryset(self):
        return RegistroActividad.objects.select_related("actor").order_by("-timestamp")


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
        convenio.created_by = self.request.user # Asigna el admin actual como creador
        convenio.save()
        messages.success(self.request, "Convenio creado exitosamente.")
        return super().form_valid(form)

class ConvenioUpdateView(StaffRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'panel/convenio_form.html'
    success_url = reverse_lazy('panel:convenio_list')

    def form_valid(self, form):
        messages.success(self.request, "Convenio actualizado exitosamente.")
        return super().form_valid(form)

class ConvenioDeleteView(StaffRequiredMixin, DeleteView):
    model = Convenio
    template_name = 'panel/convenio_confirm_delete.html'
    success_url = reverse_lazy('panel:convenio_list')

    def form_valid(self, form):
        messages.success(self.request, "Convenio eliminado exitosamente.")
        return super().form_valid(form)

class ConvenioListView(StaffRequiredMixin, ListView):
    model = Convenio
    template_name = 'panel/convenio_list.html' # Crearemos esta plantilla
    context_object_name = 'convenios'
    paginate_by = 15

class NoticiaListView(StaffRequiredMixin, ListView):
    model = Noticia
    template_name = 'panel/noticia_list.html' # Crearemos esta plantilla
    context_object_name = 'noticias'
    paginate_by = 15

class ServicioListView(StaffRequiredMixin, ListView):
    model = Servicio
    template_name = 'panel/servicio_list.html' # Crearemos esta plantilla
    context_object_name = 'servicios'
    paginate_by = 15        

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
                Q(razon_social__icontains=query) |
                Q(ruc__icontains=query) |
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(usuario__email__icontains=query)
            )
        return queryset

class SocioUpdateView(StaffRequiredMixin, UpdateView):
    model = Usuario # El modelo principal es el Usuario
    form_class = UsuarioEditForm
    template_name = 'panel/socio_form.html'
    success_url = reverse_lazy('panel:gestion_socios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos el formulario del perfil de socio al contexto
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
            messages.success(self.request, f"Socio '{self.object.get_full_name()}' actualizado exitosamente.")
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
