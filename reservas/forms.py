from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Reserva, Lugar

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['lugar', 'fecha_inicio', 'fecha_fin', 'proposito', 'descripcion', 'numero_personas']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                }
            ),
            'lugar': forms.Select(attrs={'class': 'form-control'}),
            'proposito': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Reunión de trabajo, Capacitación, etc.'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles adicionales sobre la reserva...'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'lugar': 'Lugar a reservar',
            'fecha_inicio': 'Fecha y hora de inicio',
            'fecha_fin': 'Fecha y hora de fin',
            'proposito': 'Propósito de la reserva',
            'descripcion': 'Descripción adicional',
            'numero_personas': 'Número de personas',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Solo mostrar lugares activos
        self.fields['lugar'].queryset = Lugar.objects.filter(activo=True).select_related('tipo')
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        lugar = cleaned_data.get('lugar')
        numero_personas = cleaned_data.get('numero_personas')
        
        if fecha_inicio and fecha_fin:
            # Validar que la fecha de fin sea posterior a la de inicio
            if fecha_fin <= fecha_inicio:
                raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
            
            # Validar que la fecha de inicio sea futura
            if fecha_inicio <= timezone.now():
                raise ValidationError('La fecha de inicio debe ser futura.')
            
            # Validar que no sea más de 6 meses en el futuro
            seis_meses = timezone.now() + timezone.timedelta(days=180)
            if fecha_inicio > seis_meses:
                raise ValidationError('No se pueden hacer reservas con más de 6 meses de anticipación.')
            
            # Validar horario de funcionamiento (8 AM a 10 PM)
            if fecha_inicio.hour < 8 or fecha_fin.hour > 22:
                raise ValidationError('Las reservas solo están disponibles de 8:00 AM a 10:00 PM.')
            
            # Validar duración mínima y máxima
            duracion = (fecha_fin - fecha_inicio).total_seconds() / 3600
            if duracion < 1:
                raise ValidationError('La reserva debe tener una duración mínima de 1 hora.')
            if duracion > 8:
                raise ValidationError('La reserva no puede exceder 8 horas.')
        
        if lugar and numero_personas:
            # Validar capacidad
            if numero_personas > lugar.tipo.capacidad_maxima:
                raise ValidationError(f'El número de personas ({numero_personas}) excede la capacidad máxima del lugar ({lugar.tipo.capacidad_maxima}).')
        
        if fecha_inicio and fecha_fin and lugar:
            # Verificar disponibilidad
            conflictos = Reserva.objects.filter(
                lugar=lugar,
                estado__in=['aprobada'],
                fecha_inicio__lt=fecha_fin,
                fecha_fin__gt=fecha_inicio
            )
            
            # Excluir la reserva actual si estamos editando
            if self.instance.pk:
                conflictos = conflictos.exclude(pk=self.instance.pk)
            
            if conflictos.exists():
                raise ValidationError('El lugar no está disponible en el horario seleccionado.')
        
        return cleaned_data