# panel/views.py

# Imports de la librería estándar de Python
import csv
from datetime import timedelta

# Imports de Django
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
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
    UsuarioEditForm,
    PerfilSocioForm,
    ConvenioForm,
    NoticiaForm,
    ServicioForm,
)
from .mixins import StaffRequiredMixin
from .utils import (
    registrar_actividad,
    registrar_aprobacion_solicitud,
    registrar_rechazo_solicitud,
    registrar_creacion,
    registrar_actualizacion,
    registrar_eliminacion,
)

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from usuarios.models import Usuario, PerfilSocio
from afiliaciones.models import SolicitudAfiliacion
from .models import RegistroActividad

from reservas.models import TipoLugar, Lugar, Reserva
from .forms import TipoLugarForm, LugarForm, ReservaPanelForm


# ==============================================================================
# VISTA PRINCIPAL DEL PANEL
# ==============================================================================
class DashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard Principal"

        # --- KPIs Clave ---
        try:
            total_usuarios = Usuario.objects.count()
        except:
            total_usuarios = 0
            
        try:
            total_socios = PerfilSocio.objects.filter(is_active=True).count()
        except:
            total_socios = 0
            
        try:
            solicitudes_pendientes = SolicitudAfiliacion.objects.filter(
                estado="PENDIENTE"
            ).count()
        except:
            solicitudes_pendientes = 0
            
        context["kpis"] = {
            "total_usuarios": total_usuarios,
            "total_socios": total_socios,
            "solicitudes_pendientes": solicitudes_pendientes,
        }

        # --- Datos para Gráfico: Nuevos usuarios en los últimos 7 días ---
        seven_days_ago = timezone.now() - timedelta(days=7)
        nuevos_usuarios_data = (
            Usuario.objects.filter(date_joined__gte=seven_days_ago)
            .values("date_joined__date")
            .annotate(count=Count("id"))
            .order_by("date_joined__date")
        )
        context["chart_labels"] = [
            entry["date_joined__date"].strftime("%b %d")
            for entry in nuevos_usuarios_data
        ]
        context["chart_data"] = [entry["count"] for entry in nuevos_usuarios_data]

        # --- Actividad Reciente del Administrador ---
        context["actividad_reciente"] = RegistroActividad.objects.select_related(
            "actor"
        ).filter(actor__is_staff=True)[
            :5
        ]  # Mostramos solo los 5 más recientes

        return context


#
# ==============================================================================
# VISTAS PARA AFILIACIONES
# ==============================================================================
class SolicitudesAfiliacionView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = SolicitudAfiliacion
    template_name = "panel/solicitudes_afiliacion.html"
    context_object_name = "solicitudes"
    paginate_by = 10

    def get_queryset(self):
        queryset = SolicitudAfiliacion.objects.filter(
            estado="PENDIENTE"
        ).select_related("usuario")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(razon_social__icontains=query)
                | Q(ruc__icontains=query)
                | Q(usuario__first_name__icontains=query)
                | Q(usuario__last_name__icontains=query)
                | Q(usuario__email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q", "")
        return context


class AprobarSolicitudView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        solicitud = get_object_or_404(SolicitudAfiliacion, pk=pk)
        if solicitud.estado == "PENDIENTE":
            
            # --- LÓGICA CORREGIDA ---
            # Ahora los campos 'ruc' y 'direccion' existen en el objeto 'solicitud'
            perfil_socio = PerfilSocio.objects.create(
                usuario=solicitud.usuario,
                razon_social=solicitud.razon_social,
                ruc=solicitud.ruc,
                direccion=solicitud.direccion_comercial,  # Usar el campo correcto
                tipo_plan='NATURAL',  # Valor por defecto
                is_active=True,
            )
            # --- FIN DE LA CORRECCIÓN ---

            solicitud.estado = "APROBADA"
            solicitud.fecha_revision = timezone.now()
            solicitud.revisado_por = request.user
            solicitud.save()

            # Registrar la aprobación de la solicitud
            registrar_aprobacion_solicitud(request.user, solicitud)

            messages.success(
                request, f"Solicitud de {solicitud.usuario.get_full_name()} aprobada."
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

            # Registrar actividad
            registrar_rechazo_solicitud(request.user, solicitud)

            messages.warning(
                request, f"Solicitud de {solicitud.usuario.get_full_name()} rechazada."
            )
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
        queryset = PerfilSocio.objects.select_related("usuario").order_by(
            "-fecha_afiliacion"
        )
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(razon_social__icontains=query)
                | Q(ruc__icontains=query)
                | Q(usuario__first_name__icontains=query)
                | Q(usuario__last_name__icontains=query)
                | Q(usuario__email__icontains=query)
            )
        return queryset


class SocioUpdateView(StaffRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = "panel/socio_form.html"
    success_url = reverse_lazy("panel:gestion_socios")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["perfil_form"] = PerfilSocioForm(
                self.request.POST, instance=self.object.perfil_socio
            )
        else:
            context["perfil_form"] = PerfilSocioForm(instance=self.object.perfil_socio)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        perfil_form = context["perfil_form"]
        if form.is_valid() and perfil_form.is_valid():
            form.save()
            perfil_socio = perfil_form.save()
            
            # Registrar la actualización del socio
            registrar_actualizacion(self.request.user, perfil_socio, "socio")
            
            messages.success(
                self.request, f"Socio '{self.object.get_full_name()}' actualizado."
            )
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class SocioDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = PerfilSocio
    template_name = "panel/socio_confirm_delete.html"
    success_url = reverse_lazy("panel:gestion_socios")

    def form_valid(self, form):
        """Sobrescribir form_valid para registrar la actividad antes de eliminar"""
        self.object = self.get_object()
        socio_nombre = self.object.razon_social or "Socio sin nombre"
        
        # Registrar la eliminación antes de eliminar el objeto
        registrar_eliminacion(self.request.user, self.object, "socio")
        
        messages.success(
            self.request,
            f"El perfil de socio para {socio_nombre} ha sido eliminado.",
        )
        return super().form_valid(form)


# ==============================================================================
# VISTAS CRUD PARA CONVENIOS
# ==============================================================================
class ConvenioListView(StaffRequiredMixin, ListView):
    model = Convenio
    template_name = "panel/convenio_list.html"
    context_object_name = "convenios"
    paginate_by = 10


class ConvenioCreateView(StaffRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = "panel/convenio_form.html"
    success_url = reverse_lazy("panel:convenio_list")

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
    template_name = "panel/convenio_form.html"
    success_url = reverse_lazy("panel:convenio_list")

    def form_valid(self, form):
        # Registrar actividad
        registrar_actualizacion(self.request.user, form.instance, "convenio")

        messages.success(self.request, "Convenio actualizado exitosamente.")
        return super().form_valid(form)


class ConvenioDeleteView(StaffRequiredMixin, DeleteView):
    model = Convenio
    template_name = "panel/convenio_confirm_delete.html"
    success_url = reverse_lazy("panel:convenio_list")

    def form_valid(self, form):
        """Sobrescribir form_valid para registrar la actividad antes de eliminar"""
        self.object = self.get_object()
        
        # Registrar la eliminación antes de eliminar el objeto
        registrar_eliminacion(self.request.user, self.object, "convenio")
        
        messages.success(self.request, "Convenio eliminado exitosamente.")
        return super().form_valid(form)


# ==============================================================================
# VISTAS CRUD PARA NOTICIAS
# ==============================================================================
class NoticiaPanelListView(StaffRequiredMixin, ListView):
    model = Noticia
    template_name = "panel/noticia_list.html"
    context_object_name = "noticias"
    paginate_by = 10


class NoticiaCreateView(StaffRequiredMixin, CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = "panel/noticia_form.html"
    success_url = reverse_lazy("panel:noticia_panel_list")

    def form_valid(self, form):
        noticia = form.save(commit=False)
        noticia.autor = self.request.user
        noticia.save()
        
        # Registrar la creación de la noticia
        registrar_creacion(self.request.user, noticia, "noticia")
        
        messages.success(self.request, "Noticia creada exitosamente.")
        return redirect(self.success_url)


class NoticiaUpdateView(StaffRequiredMixin, UpdateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = "panel/noticia_form.html"
    success_url = reverse_lazy("panel:noticia_panel_list")

    def form_valid(self, form):
        # Registrar la actualización de la noticia
        registrar_actualizacion(self.request.user, form.instance, "noticia")
        
        messages.success(self.request, "Noticia actualizada exitosamente.")
        return super().form_valid(form)


class NoticiaDeleteView(StaffRequiredMixin, DeleteView):
    model = Noticia
    template_name = "panel/noticia_confirm_delete.html"
    success_url = reverse_lazy("panel:noticia_panel_list")

    def form_valid(self, form):
        """Sobrescribir form_valid para registrar la actividad antes de eliminar"""
        self.object = self.get_object()
        
        # Registrar la eliminación antes de eliminar el objeto
        registrar_eliminacion(self.request.user, self.object, "noticia")
        
        messages.success(
            self.request, f"La noticia '{self.object.titulo}' ha sido eliminada."
        )
        return super().form_valid(form)


# ==============================================================================
# VISTAS CRUD PARA SERVICIOS
# ==============================================================================
class ServicioPanelListView(StaffRequiredMixin, ListView):
    model = Servicio
    template_name = "panel/servicio_list.html"
    context_object_name = "servicios"
    paginate_by = 10


class ServicioCreateView(StaffRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "panel/servicio_form.html"
    success_url = reverse_lazy("panel:servicio_panel_list")

    def form_valid(self, form):
        servicio = form.save(commit=False)
        servicio.creado_por = self.request.user
        servicio.save()
        
        # Registrar la creación del servicio
        registrar_creacion(self.request.user, servicio, "servicio")
        
        messages.success(self.request, "Servicio creado exitosamente.")
        return super().form_valid(form)


class ServicioUpdateView(StaffRequiredMixin, UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = "panel/servicio_form.html"
    success_url = reverse_lazy("panel:servicio_panel_list")

    def form_valid(self, form):
        # Registrar la actualización del servicio
        registrar_actualizacion(self.request.user, form.instance, "servicio")
        
        messages.success(self.request, "Servicio actualizado exitosamente.")
        return super().form_valid(form)


class ServicioDeleteView(StaffRequiredMixin, DeleteView):
    model = Servicio
    template_name = "panel/servicio_confirm_delete.html"
    success_url = reverse_lazy("panel:servicio_panel_list")

    def form_valid(self, form):
        """Sobrescribir form_valid para registrar la actividad antes de eliminar"""
        self.object = self.get_object()
        
        # Registrar la eliminación antes de eliminar el objeto
        registrar_eliminacion(self.request.user, self.object, "servicio")
        
        messages.success(
            self.request, f"El servicio '{self.object.nombre}' ha sido eliminado."
        )
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
        # Solo mostrar actividades de usuarios administradores (staff)
        queryset = (
            RegistroActividad.objects.select_related("actor", "content_type")
            .filter(actor__is_staff=True)
            .order_by("-timestamp")
        )

        # Filtro de búsqueda
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(accion__icontains=query)
                | Q(actor__first_name__icontains=query)
                | Q(actor__last_name__icontains=query)
                | Q(actor__email__icontains=query)
            )

        # Filtro por tipo de contenido
        content_type = self.request.GET.get("tipo")
        if content_type:
            queryset = queryset.filter(content_type__model=content_type)

        # Filtro por fecha
        fecha = self.request.GET.get("fecha")
        if fecha:
            try:
                from datetime import datetime

                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
                queryset = queryset.filter(timestamp__date=fecha_obj)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_query"] = self.request.GET.get("q", "")
        context["current_tipo"] = self.request.GET.get("tipo", "")
        context["current_fecha"] = self.request.GET.get("fecha", "")

        # Estadísticas adicionales (solo de administradores)
        from django.utils import timezone

        today = timezone.now().date()
        context["actividades_hoy"] = RegistroActividad.objects.filter(
            timestamp__date=today, actor__is_staff=True
        ).count()

        return context


from .forms import AfiliacionAdminForm


class SolicitudAfiliacionDetailView(StaffRequiredMixin, UpdateView):
    model = SolicitudAfiliacion
    form_class = AfiliacionAdminForm
    template_name = 'panel/solicitud_detail.html'
    context_object_name = 'solicitud'
    success_url = reverse_lazy('panel:solicitudes_afiliacion')

    def form_valid(self, form):
        solicitud = form.save(commit=False)
        solicitud.revisado_por = self.request.user
        solicitud.fecha_revision = timezone.now()
        
        if solicitud.estado == 'APROBADA':
            # --- VALIDACIÓN AÑADIDA ---
            # 1. Comprueba si el usuario ya tiene un perfil de socio.
            if hasattr(solicitud.usuario, 'perfil_socio'):
                messages.warning(self.request, f"Este usuario ya tiene un perfil de socio.")
                return redirect(self.get_success_url())

            # 2. Comprueba si el RUC ya está siendo utilizado por OTRO socio.
            if PerfilSocio.objects.filter(ruc=solicitud.ruc).exists():
                messages.error(self.request, f"Error: El RUC '{solicitud.ruc}' ya está registrado por otro socio.")
                return self.render_to_response(self.get_context_data(form=form))
            # --- FIN DE LA VALIDACIÓN ---

            # Si pasa las validaciones, crea el perfil.
            PerfilSocio.objects.create(
                usuario=solicitud.usuario,
                razon_social=solicitud.razon_social,
                ruc=solicitud.ruc,
                direccion=solicitud.direccion_comercial,
                is_active=True
            )
            messages.success(self.request, f"Solicitud aprobada. Se ha creado el perfil de socio para {solicitud.usuario.get_full_name()}.")
        
        elif solicitud.estado == 'RECHAZADA':
            messages.warning(self.request, f"La solicitud de {solicitud.usuario.get_full_name()} ha sido rechazada.")

        solicitud.save()
        return redirect(self.get_success_url())


# ==============================================================================
# VISTAS CRUD PARA RESERVAS
# ==============================================================================


# --- Gestión de Tipos de Lugar ---
class TipoLugarListView(StaffRequiredMixin, ListView):
    model = TipoLugar
    template_name = "panel/tipo_lugar_list.html"
    context_object_name = "tipos_lugar"


class TipoLugarCreateView(StaffRequiredMixin, CreateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = "panel/tipo_lugar_form.html"
    success_url = reverse_lazy("panel:tipo_lugar_list")


class TipoLugarUpdateView(StaffRequiredMixin, UpdateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = "panel/tipo_lugar_form.html"
    success_url = reverse_lazy("panel:tipo_lugar_list")


# --- Gestión de Lugares ---
class LugarListView(StaffRequiredMixin, ListView):
    model = Lugar
    template_name = "panel/lugar_list.html"
    context_object_name = "lugares"


class LugarCreateView(StaffRequiredMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = "panel/lugar_form.html"
    success_url = reverse_lazy("panel:lugar_list")


class LugarUpdateView(StaffRequiredMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = "panel/lugar_form.html"
    success_url = reverse_lazy("panel:lugar_list")


# --- Gestión de Reservas ---
class ReservaPanelListView(StaffRequiredMixin, ListView):
    model = Reserva
    template_name = "panel/reserva_list.html"
    context_object_name = "reservas"
    paginate_by = 15


class ReservaPanelUpdateView(StaffRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaPanelForm
    template_name = "panel/reserva_form.html"
    success_url = reverse_lazy("panel:reserva_panel_list")

    def form_valid(self, form):
        reserva = form.save(commit=False)
        if "estado" in form.changed_data and form.cleaned_data["estado"] == "aprobada":
            reserva.aprobada_por = self.request.user
            reserva.fecha_aprobacion = timezone.now()
        reserva.save()
        messages.success(self.request, "Reserva actualizada exitosamente.")
        return super().form_valid(form)


class ReservaPanelDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Reserva
    template_name = "panel/reserva_confirm_delete.html"
    success_url = reverse_lazy("panel:reserva_panel_list")
    context_object_name = "reserva"

    def form_valid(self, form):
        # Registrar la actividad antes de eliminar
        registrar_eliminacion(
            self.request.user,
            self.object,
            f"reserva #{self.object.id} - {self.object.lugar.nombre}"
        )
        # Mostrar mensaje de éxito
        messages.success(self.request, "La reserva ha sido eliminada exitosamente.")
        # Eliminar la reserva
        return super().form_valid(form)


def aprobar_reserva(request, pk):
    if not request.user.is_staff:
        return redirect('panel:reserva_panel_list')
    
    reserva = get_object_or_404(Reserva, pk=pk)
    
    if reserva.estado == 'pendiente':
        reserva.estado = 'confirmada'
        reserva.save()
        
        # Registrar la actividad
        registrar_actividad(
            request.user,
            f"Aprobó la reserva #{reserva.id} - {reserva.lugar.nombre}",
            reserva
        )
        
        messages.success(request, "La reserva ha sido aprobada exitosamente.")
    else:
        messages.warning(request, "Solo se pueden aprobar reservas que estén en estado 'Pendiente'.")
    
    return redirect('panel:reserva_panel_list')


def rechazar_reserva(request, pk):
    if not request.user.is_staff:
        return redirect('panel:reserva_panel_list')
    
    reserva = get_object_or_404(Reserva, pk=pk)
    
    if reserva.estado == 'pendiente':
        reserva.estado = 'rechazada'
        reserva.save()
        
        # Registrar la actividad
        registrar_actividad(
            request.user,
            f"Rechazó la reserva #{reserva.id} - {reserva.lugar.nombre}",
            reserva
        )
        
        messages.success(request, "La reserva ha sido rechazada.")
    else:
        messages.warning(request, "Solo se pueden rechazar reservas que estén en estado 'Pendiente'.")
    
    return redirect('panel:reserva_panel_list')
