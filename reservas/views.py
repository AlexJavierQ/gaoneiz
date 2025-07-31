# reservas/views.py

import json
from django.core.serializers.json import DjangoJSONEncoder # 1. IMPORTAR EL CODIFICADOR
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin

from .models import Lugar, Reserva
from .forms import ReservaForm, LugarForm

# ==============================================================================
# VISTAS PÚBLICAS (PARA SOCIOS)
# ==============================================================================

class LugarListView(ListView):
    model = Lugar
    template_name = 'reservas/lugares_list.html'
    context_object_name = 'lugares'

    def get_queryset(self):
        """
        CORREGIDO: Filtra para mostrar solo lugares y tipos de lugar que estén activos.
        """
        # --- CAMBIO AQUÍ: Se añade el filtro por lugar.activo ---
        return Lugar.objects.filter(activo=True, tipo__activo=True).select_related('tipo')


class LugarDetailView(DetailView):
    model = Lugar
    template_name = 'reservas/lugar_detail.html'
    context_object_name = 'lugar'


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'reservas/reserva_form.html'
    success_url = reverse_lazy('reservas:mis_reservas')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['lugar'].queryset = Lugar.objects.filter(tipo__activo=True)
        return form

    def get_initial(self):
        initial = super().get_initial()
        lugar_id = self.request.GET.get('lugar')
        if lugar_id:
            try:
                lugar = Lugar.objects.get(pk=lugar_id, tipo__activo=True)
                initial['lugar'] = lugar
            except Lugar.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lugares_qs = Lugar.objects.filter(tipo__activo=True).values(
            'id',
            'nombre',
            'tipo__capacidad_maxima',
            'tipo__precio_por_hora'
        )
        # 2. USAR EL CODIFICADOR PARA MANEJAR TIPOS DECIMAL
        context['lugares_data_json'] = json.dumps(list(lugares_qs), cls=DjangoJSONEncoder)
        return context

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, "Tu solicitud de reserva ha sido enviada con éxito.")
        return super().form_valid(form)


class MisReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/mis_reservas.html"
    context_object_name = "reservas"
    paginate_by = 10

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related(
            "lugar", "lugar__tipo"
        ).order_by('-fecha_inicio')


class ReservaDetailView(LoginRequiredMixin, DetailView):
    model = Reserva
    template_name = "reservas/reserva_detail.html"
    context_object_name = "reserva"

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user).select_related(
            "lugar", "lugar__tipo", "usuario"
        )


@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    if reserva.estado in ["pendiente", "aprobada"]:
        reserva.estado = "cancelada"
        reserva.save()
        messages.success(request, "Reserva cancelada exitosamente.")
    else:
        messages.error(request, f"No se puede cancelar una reserva en estado '{reserva.estado}'.")
    return redirect("reservas:mis_reservas")

# ==============================================================================
# VISTA PARA AJAX
# ==============================================================================
@login_required
def verificar_disponibilidad(request):
    if request.method == "GET":
        lugar_id = request.GET.get("lugar_id")
        fecha_inicio = request.GET.get("fecha_inicio")
        fecha_fin = request.GET.get("fecha_fin")

        if lugar_id and fecha_inicio and fecha_fin:
            try:
                lugar = Lugar.objects.get(id=lugar_id)
                conflictos = Reserva.objects.filter(
                    lugar=lugar,
                    fecha_inicio__lt=fecha_fin,
                    fecha_fin__gt=fecha_inicio,
                ).exclude(estado='cancelada').exists()
                return JsonResponse({"disponible": not conflictos})
            except Lugar.DoesNotExist:
                pass
    return JsonResponse({"disponible": False, "mensaje": "Datos de consulta inválidos"}, status=400)


# ==============================================================================
# VISTAS DEL PANEL DE ADMINISTRACIÓN (Mover a 'panel.views' en el futuro)
# ==============================================================================
class LugarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'panel/lugar_form.html'
    success_url = reverse_lazy('panel:lugar_list')
    success_message = "Lugar creado exitosamente."


class LugarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = 'panel/lugar_form.html'
    success_url = reverse_lazy('panel:lugar_list')
    success_message = "Lugar actualizado exitosamente."