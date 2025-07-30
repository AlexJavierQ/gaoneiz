# panel/forms.py

from django import forms
from convenios.models import Convenio
from afiliaciones.models import SolicitudAfiliacion
from usuarios.models import Usuario, PerfilSocio
from noticias.models import Noticia
from servicios.models import Servicio
from reservas.models import TipoLugar, Lugar, Reserva # <-- Nuevas importaciones


class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = [
            "nombre_empresa",
            "categoria",
            "descripcion",
            "estado",
            "fecha_inicio",
            "fecha_vencimiento",
            "sitio_web",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "fecha_vencimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "descripcion": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "nombre_empresa": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "sitio_web": forms.URLInput(attrs={"class": "form-control"}),
        }


class UsuarioEditForm(forms.ModelForm):
    """Formulario para editar los datos base del usuario."""

    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "email",
            "cedula",
            "telefono",
            "is_staff",
            "is_active",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "cedula": forms.TextInput(attrs={"class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PerfilSocioForm(forms.ModelForm):
    """Formulario para editar los datos del perfil de socio."""

    class Meta:
        model = PerfilSocio
        fields = ["razon_social", "ruc", "direccion", "tipo_plan", "is_active"]
        widgets = {
            "razon_social": forms.TextInput(attrs={"class": "form-control"}),
            "ruc": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "tipo_plan": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {"is_active": "¿Es un socio activo?"}


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ["titulo", "resumen", "contenido", "imagen", "categoria", "publicada"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "resumen": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
            "categoria": forms.TextInput(attrs={"class": "form-control"}),
            "publicada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {"publicada": "¿Publicar esta noticia?"}


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        # --- CORRECCIÓN AQUÍ ---
        # Cambiamos 'exclusivo_para_socios' por 'solo_socios', que es el nombre correcto en el modelo.
        fields = ['nombre', 'descripcion', 'categoria', 'solo_socios', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'solo_socios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'solo_socios': '¿Este servicio es exclusivo para socios?',
            'activo': '¿Este servicio está activo y visible?'
        }


# Formulario para que el admin gestione las solicitudes
class AfiliacionAdminForm(forms.ModelForm):
    class Meta:
        model = SolicitudAfiliacion
        fields = ["estado"]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

class TipoLugarForm(forms.ModelForm):
    class Meta:
        model = TipoLugar
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_por_hora': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'equipamiento': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReservaPanelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['lugar', 'usuario', 'fecha_inicio', 'fecha_fin', 'proposito', 'estado', 'notas_admin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'lugar': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'proposito': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'notas_admin': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }