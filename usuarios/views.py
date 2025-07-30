from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .forms import CustomSignupForm
from .models import Usuario, PerfilSocio


class CustomSignupView(CreateView):
    """Vista personalizada para el registro de usuarios."""

    model = Usuario
    form_class = CustomSignupForm
    template_name = "account/signup.html"
    success_url = reverse_lazy("web:home")

    def form_valid(self, form):
        """Procesa el formulario válido y autentica al usuario."""
        response = super().form_valid(form)
        # Autenticar automáticamente al usuario después del registro
        # Especificamos el backend para evitar errores con múltiples backends
        login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        messages.success(
            self.request, "¡Bienvenido! Tu cuenta ha sido creada exitosamente."
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear Cuenta"
        return context


class SociosListView(ListView):
    """Vista para mostrar el directorio de socios activos."""

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
