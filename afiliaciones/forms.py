# afiliaciones/forms.py
from django import forms
from .models import SolicitudAfiliacion

class SolicitudAfiliacionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAfiliacion
        # Excluimos los campos que se llenan automáticamente o que maneja el admin.
        # Django incluirá todos los demás campos del modelo en el formulario.
        exclude = [
            'usuario', 
            'estado', 
            'fecha_solicitud', 
            'fecha_revision', 
            'revisado_por'
        ]
        
    def __init__(self, *args, **kwargs):
        """
        Este método añade automáticamente las clases de Bootstrap a todos los campos
        para que se vean bien sin necesidad de crispy-forms.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})