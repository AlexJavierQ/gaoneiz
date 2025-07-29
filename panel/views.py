# panel/views.py
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .mixins import StaffRequiredMixin
from .models import RegistroActividad
from afiliaciones.models import SolicitudAfiliacion
from usuarios.models import Usuario, PerfilSocio


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
    paginate_by = 20

    def get_queryset(self):
        return SolicitudAfiliacion.objects.select_related("usuario").order_by(
            "-fecha_solicitud"
        )


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
