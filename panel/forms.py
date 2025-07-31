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
            "imagen",
        ]
        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_vencimiento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "imagen": forms.FileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "nombre_empresa": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "sitio_web": forms.URLInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen'].required = False

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
        # --- CAMBIO AQUÍ: Se añade 'imagen' a la lista de campos ---
        fields = ['nombre', 'descripcion', 'categoria', 'precio', 'solo_socios', 'activo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'solo_socios': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # --- CAMBIO AQUÍ: Se añade un widget para el campo de imagen ---
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
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
        # --- CAMBIO AQUÍ: Se añade 'activo' a la lista de campos ---
        fields = ['nombre', 'tipo', 'descripcion', 'imagen', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            # --- CAMBIO AQUÍ: Se añade un widget para el campo 'activo' ---
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ReservaPanelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        # --- LÍNEA CORREGIDA ---
        # Asegúrate de que estos campos existan en tu modelo 'Reserva'
        fields = ['usuario', 'lugar', 'fecha_inicio', 'fecha_fin', 'estado', 'notas_adicionales']
        
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['fecha_fin'].input_formats = ('%Y-%m-%dT%H:%M',)