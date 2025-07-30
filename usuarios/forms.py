from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, PerfilSocio    
from allauth.account.forms import SignupForm # <-- Importamos el formulario base de allauth

class CustomSignupForm(SignupForm):
    """
    Formulario de registro personalizado que hereda de allauth
    y añade los campos de nombre y apellido.
    """
    first_name = forms.CharField(max_length=30, label='Nombre', widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(max_length=30, label='Apellido', widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))

    def save(self, request):
        # Llama al método save original de allauth para crear el usuario
        user = super(CustomSignupForm, self).save(request)
        # Guarda los campos adicionales en el nuevo objeto de usuario
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class PerfilForm(forms.ModelForm):
    """Formulario para que un usuario edite su información básica."""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cedula', 'telefono']

class PerfilSocioForm(forms.ModelForm):
    """Formulario para que un socio edite la información de su perfil."""
    class Meta:
        model = PerfilSocio
        fields = ['razon_social', 'ruc', 'direccion']        