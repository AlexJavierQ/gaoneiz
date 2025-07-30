from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from .forms import CustomSignupForm, PerfilForm, PerfilSocioForm
from .models import Usuario, PerfilSocio


class CustomSignupView(CreateView):
    """Vista personalizada para el registro de nuevos usuarios."""

    model = Usuario
    form_class = CustomSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("web:home")

    def form_valid(self, form):
        """Autentica al usuario tras un registro exitoso."""
        response = super().form_valid(form)
        login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend"
        )
        messages.success(
            self.request,
            "¡Bienvenido! Tu cuenta ha sido creada exitosamente."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Cuenta"
        return context


class SociosListView(ListView):
    """Muestra el directorio público de socios activos."""

    model = PerfilSocio
    template_name = "usuarios/socios_list.html"
    context_object_name = "socios"
    paginate_by = 12

    def get_queryset(self):
        return (
            PerfilSocio.objects.filter(is_active=True)
            .select_related("usuario")
            .order_by("razon_social")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Directorio de Socios"
        return context


class PerfilView(LoginRequiredMixin, DetailView):
    """Muestra el perfil del usuario autenticado."""

    model = Usuario
    template_name = "usuarios/perfil.html"
    context_object_name = "usuario"

    def get_object(self, queryset=None):
        return self.request.user


class EditarPerfilView(LoginRequiredMixin, UpdateView):
    """Permite al usuario editar su perfil (y perfil de socio si aplica)."""

    model = Usuario
    form_class = PerfilForm
    template_name = "usuarios/editar_perfil.html"
    success_url = reverse_lazy("usuarios:perfil")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, "perfil_socio"):
            if self.request.method == "POST":
                context["perfil_socio_form"] = PerfilSocioForm(
                    self.request.POST,
                    instance=self.request.user.perfil_socio
                )
            else:
                context["perfil_socio_form"] = PerfilSocioForm(
                    instance=self.request.user.perfil_socio
                )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        perfil_socio_form = context.get("perfil_socio_form")

        if perfil_socio_form and perfil_socio_form.is_valid():
            perfil_socio_form.save()

        messages.success(self.request, "Perfil actualizado exitosamente.")
        return super().form_valid(form)
