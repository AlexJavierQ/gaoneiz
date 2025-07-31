from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from .models import Lugar, Reserva, TipoLugar
from .forms import ReservaForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from reservas.models import Lugar, TipoLugar, Reserva
from reservas.forms import LugarForm, TipoLugarForm, ReservaPanelForm
from django.views.generic import ListView, DetailView
from .models import Lugar, Reserva
class LugarListView(ListView):
    model = Lugar
    template_name = 'reservas/lugares_list.html'
    context_object_name = 'lugares'

    def get_queryset(self):
        """
        CORREGIDO: Filtra los lugares para mostrar solo aquellos
        cuyo Tipo de Lugar está activo.
        """
        # Se usa 'tipo__activo=True' para acceder al campo del modelo relacionado.
        return Lugar.objects.filter(tipo__activo=True).select_related('tipo')


class LugarDetailView(DetailView):
    model = Lugar
    template_name = 'reservas/lugar_detail.html' # Asegúrate que este sea tu template
    context_object_name = 'lugar'        
class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'  # Asegúrate que este sea tu template
    success_url = reverse_lazy('reservas:mis_reservas') # URL a donde ir después de reservar

    def get_form(self, form_class=None):
        """
        Sobrescribe el método para filtrar el queryset del campo 'lugar'.
        """
        form = super().get_form(form_class)
        
        # --- CORRECCIÓN AQUÍ ---
        # Filtra el campo 'lugar' para mostrar solo aquellos cuyo 'TipoLugar' está activo.
        # Se usa 'tipo__activo=True' para consultar a través de la relación.
        form.fields['lugar'].queryset = Lugar.objects.filter(tipo__activo=True)
        
        return form

    def get_initial(self):
        """
        Pre-selecciona el lugar si se pasa como parámetro en la URL.
        (Ej: /reservas/nueva/?lugar=1)
        """
        initial = super().get_initial()
        lugar_id = self.request.GET.get('lugar')
        if lugar_id:
            try:
                # Se asegura que el lugar exista y esté activo antes de seleccionarlo.
                lugar = Lugar.objects.get(pk=lugar_id, tipo__activo=True)
                initial['lugar'] = lugar
            except Lugar.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        """
        Asigna el usuario logueado a la reserva antes de guardarla.
        """
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class MisReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario es socio
        if request.user.is_authenticated and not request.user.es_socio:
            messages.info(
                request,
                "Para ver tus reservas necesitas ser socio. ¡Afíliate ahora y accede a todos nuestros beneficios!",
            )
            return redirect("afiliaciones:solicitar_afiliacion")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related(
            "lugar", "lugar__tipo"
        )


class ReservaDetailView(LoginRequiredMixin, DetailView):
    model = Reserva
    template_name = "reservas/reserva_detail.html"
    context_object_name = "reserva"

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario es socio
        if request.user.is_authenticated and not request.user.es_socio:
            messages.info(
                request,
                "Para acceder a los detalles de reservas necesitas ser socio. ¡Completa tu afiliación!",
            )
            return redirect("afiliaciones:solicitar_afiliacion")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related(
            "lugar", "lugar__tipo", "aprobada_por"
        )


@login_required
def cancelar_reserva(request, pk):
    # Verificar si el usuario es socio
    if not request.user.es_socio:
        messages.warning(
            request,
            "Solo los socios pueden gestionar reservas. ¡Afíliate para acceder a este beneficio!",
        )
        return redirect("afiliaciones:solicitar_afiliacion")

    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)

    if reserva.estado in ["pendiente", "aprobada"]:
        reserva.estado = "cancelada"
        reserva.save()
        messages.success(request, "Reserva cancelada exitosamente.")
    else:
        messages.error(request, "No se puede cancelar esta reserva.")

    return redirect("reservas:mis_reservas")


# Vista para mostrar disponibilidad (AJAX)
@login_required
def verificar_disponibilidad(request):
    if request.method == "GET":
        lugar_id = request.GET.get("lugar_id")
        fecha_inicio = request.GET.get("fecha_inicio")
        fecha_fin = request.GET.get("fecha_fin")

        if lugar_id and fecha_inicio and fecha_fin:
            try:
                lugar = Lugar.objects.get(id=lugar_id)

                # Verificar conflictos con reservas aprobadas
                conflictos = Reserva.objects.filter(
                    lugar=lugar,
                    estado="aprobada",
                    fecha_inicio__lt=fecha_fin,
                    fecha_fin__gt=fecha_inicio,
                ).exists()

                return JsonResponse(
                    {
                        "disponible": not conflictos,
                        "mensaje": (
                            "Disponible"
                            if not conflictos
                            else "No disponible en ese horario"
                        ),
                    }
                )
            except Lugar.DoesNotExist:
                pass

    return JsonResponse({"disponible": False, "mensaje": "Error en la consulta"})

class LugarCreateView(SuccessMessageMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'panel/lugar_form.html'
    success_url = reverse_lazy('panel:lugar_list')
    success_message = "Lugar creado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nuevo Lugar"
        return context

# --- VISTA PARA ACTUALIZAR LUGAR (NO NECESITA CAMBIOS VISIBLES) ---
# Django's UpdateView también maneja request.FILES automáticamente.
class LugarUpdateView(SuccessMessageMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'panel/lugar_form.html'
    success_url = reverse_lazy('panel:lugar_list')
    success_message = "Lugar actualizado exitosamente."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Lugar"
        return context
