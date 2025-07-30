from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class TipoLugar(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    capacidad_maxima = models.PositiveIntegerField()
    precio_por_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Lugar"
        verbose_name_plural = "Tipos de Lugares"
    
    def __str__(self):
        return self.nombre

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoLugar, on_delete=models.CASCADE, related_name='lugares')
    ubicacion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    equipamiento = models.TextField(blank=True, help_text="Equipos y recursos disponibles")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo.nombre})"

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    proposito = models.CharField(max_length=200, help_text="Propósito de la reserva")
    descripcion = models.TextField(blank=True, help_text="Detalles adicionales")
    numero_personas = models.PositiveIntegerField(default=1)
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campos para gestión administrativa
    aprobada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reservas_aprobadas',
        limit_choices_to={'is_staff': True}
    )
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    notas_admin = models.TextField(blank=True, help_text="Notas del administrador")
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Reserva de {self.usuario.get_full_name()} - {self.lugar.nombre} ({self.get_estado_display()})"
    
    @property
    def duracion_horas(self):
        """Calcula la duración en horas"""
        delta = self.fecha_fin - self.fecha_inicio
        return delta.total_seconds() / 3600
    
    @property
    def costo_total(self):
        """Calcula el costo total basado en las horas y precio por hora"""
        return self.duracion_horas * float(self.lugar.tipo.precio_por_hora)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validar que la fecha de fin sea posterior a la de inicio
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        
        # Validar que la fecha de inicio sea futura (solo para nuevas reservas)
        if not self.pk and self.fecha_inicio <= timezone.now():
            raise ValidationError('La fecha de inicio debe ser futura.')
        
        # Validar capacidad
        if self.numero_personas > self.lugar.tipo.capacidad_maxima:
            raise ValidationError(f'El número de personas ({self.numero_personas}) excede la capacidad máxima del lugar ({self.lugar.tipo.capacidad_maxima}).')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)