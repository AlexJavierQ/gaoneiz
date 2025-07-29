# panel/forms.py

from django import forms
from convenios.models import Convenio, Beneficio
from afiliaciones.models import SolicitudAfiliacion
from usuarios.models import Usuario, PerfilSocio

# --- AÑADE ESTE NUEVO FORMULARIO ---
class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = [
            'nombre_empresa', 'categoria', 'descripcion', 'estado', 
            'fecha_inicio', 'fecha_vencimiento', 'sitio_web'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
        }
     

class UsuarioEditForm(forms.ModelForm):
    """Formulario para editar los datos base del usuario."""
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'cedula', 'telefono', 'is_staff', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PerfilSocioForm(forms.ModelForm):
    """Formulario para editar los datos del perfil de socio."""
    class Meta:
        model = PerfilSocio
        fields = ['razon_social', 'ruc', 'direccion', 'tipo_plan', 'is_active']
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tipo_plan': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_active': '¿Es un socio activo?'
        }        