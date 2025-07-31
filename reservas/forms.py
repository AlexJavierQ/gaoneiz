# reservas/forms.py

from django import forms
from .models import Lugar, TipoLugar, Reserva


class TipoLugarForm(forms.ModelForm):
    class Meta:
        model = TipoLugar
        fields = ["nombre", "capacidad_maxima", "precio_por_hora", "activo"]


class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ["nombre", "tipo", "descripcion", "imagen"]


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["lugar", "fecha_inicio", "fecha_fin", "proposito", "notas_adicionales"]
        widgets = {
            "fecha_inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "fecha_fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "proposito": forms.TextInput(attrs={
                "placeholder": "Ej: Reunión de equipo, Capacitación, etc.",
                "required": "required"
            }),
        }

    def __init__(self, *args, **kwargs):
        # Se extrae el 'user' de los kwargs ANTES de continuar.
        user = kwargs.pop('user', None)
        
        # Se llama al __init__ de la clase padre con los kwargs ya limpios.
        super().__init__(*args, **kwargs)
        
        # Se aplica el formato a los campos de fecha.
        self.fields["fecha_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["fecha_fin"].input_formats = ("%Y-%m-%dT%H:%M",)


class ReservaPanelForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            "usuario",
            "lugar",
            "fecha_inicio",
            "fecha_fin",
            "proposito",
            "estado",
            "notas_adicionales",
        ]
        widgets = {
            "fecha_inicio": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "fecha_fin": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "proposito": forms.TextInput(attrs={"placeholder": "Ej: Reunión de equipo"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_inicio"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["fecha_fin"].input_formats = ("%Y-%m-%dT%H:%M",)
        # Configurar el campo proposito
        self.fields['proposito'].required = True
        self.fields['proposito'].label = 'Propósito de la reserva *'
        self.fields['proposito'].help_text = 'Por favor, indique el propósito de la reserva'
        self.fields['proposito'].widget.attrs.update({
            'placeholder': 'Ej: Reunión de equipo, Capacitación, etc.'
        })