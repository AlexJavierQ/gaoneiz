# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

# ==============================================================================
# 1. MODELOS BASE DE USUARIOS
# ==============================================================================
from app_camara_comercio.managers import PersonaManager  

from app_camara_comercio.managers import PersonaManager  # asegúrate que esta importación es correcta

class Persona(AbstractUser):
    """
    Modelo base que extiende el usuario de Django.
    Será la clase padre para Administradores y Afiliados.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre de usuario",
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True)
    cedula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telf = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="persona_set",
        related_query_name="persona",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="persona_set",
        related_query_name="persona",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    objects = PersonaManager()  # ✅ Aquí va el manager personalizado, fuera de cualquier campo

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"

    def __str__(self):
        return self.get_full_name() or self.email

class Administrador(Persona):
    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def save(self, *args, **kwargs):
        self.is_staff = True
        super().save(*args, **kwargs)

# ==============================================================================
# 2. MODELOS DE AFILIADOS Y DOCUMENTACIÓN
# ==============================================================================

class Afiliado(Persona):
    TIPO_PLAN_CHOICES = [
        ('persona_natural', 'Plan Persona Natural'),
        ('empresa', 'Plan Empresa'),
        ('entidad_financiera', 'Plan Entidad Financiera'),
    ]
    TIPO_NEGOCIO_CHOICES = [
        ('comercio', 'Comercio'),
        ('servicios', 'Servicios'),
        ('importacion_exportacion', 'Importación/Exportación'),
        ('industria', 'Industria'),
        ('otro', 'Otro'),
    ]
    RED_SOCIAL_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('youtube', 'Youtube'),
        ('tiktok', 'Tik Tok'),
    ]

    tipo_plan = models.CharField(max_length=20, choices=TIPO_PLAN_CHOICES, verbose_name="Tipo de Plan")
    fecha_afiliacion = models.DateField(auto_now_add=True, verbose_name="Fecha de afiliación")
    nombre_comercial = models.CharField(max_length=200, verbose_name="Nombre Comercial", blank=True, null=True)
    RUC = models.CharField(max_length=20, verbose_name="RUC", blank=True, null=True)
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social", blank=True, null=True)
    nombre_representante_legal = models.CharField(max_length=200, verbose_name="Representante Legal", blank=True, null=True)
    cedula_representante = models.CharField(max_length=20, verbose_name="Cédula Representante Legal", blank=True, null=True)
    fecha_visita = models.DateField(verbose_name="Fecha de visita", blank=True, null=True)
    red_social_preferida = models.CharField(max_length=20, choices=RED_SOCIAL_CHOICES, verbose_name="Red social que más usa", blank=True, null=True)
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad", blank=True, null=True)
    tipo_negocio = models.CharField(max_length=30, choices=TIPO_NEGOCIO_CHOICES, verbose_name="Tipo de Negocio", blank=True, null=True)
    acepta_terminos = models.BooleanField(default=False, verbose_name="Acepto los términos y condiciones")

    def save(self, *args, **kwargs):
        if not self.pk: 
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.razon_social or self.get_full_name()}"

    class Meta:
        verbose_name = "Afiliado"
        verbose_name_plural = "Afiliados"

class DocumentosAfiliado(models.Model):
    afiliado = models.OneToOneField(Afiliado, on_delete=models.CASCADE, related_name='documentos')
    titular_nombres = models.CharField(max_length=200, verbose_name="Nombres Completos Titular")
    titular_telefono = models.CharField(max_length=20, verbose_name="Teléfono Titular")
    titular_cedula = models.CharField(max_length=20, verbose_name="Cédula Titular")
    beneficiario_nombres = models.CharField(max_length=200, verbose_name="Nombres Completos Beneficiario")
    beneficiario_porcentaje = models.PositiveIntegerField(verbose_name="Porcentaje Beneficiario")
    copia_ruc = models.FileField(upload_to='documentos/ruc/', verbose_name="Copia de RUC")
    copia_cedula = models.FileField(upload_to='documentos/cedula/', verbose_name="Copia de Cédula", blank=True, null=True)
    copia_nombramiento = models.FileField(upload_to='documentos/nombramiento/', verbose_name="Copia de Nombramiento", blank=True, null=True)
    firma_electronica = models.FileField(upload_to='documentos/firmas/', verbose_name="Firma Electrónica")
    consentimiento_datos = models.BooleanField(default=False, verbose_name="Consentimiento Protección de Datos")

    def __str__(self):
        return f"Documentos de {self.afiliado}"

    class Meta:
        verbose_name = "Documentos de Afiliado"
        verbose_name_plural = "Documentos de Afiliados"

# ==============================================================================
# 3. MODELOS DE CONVENIOS Y BENEFICIOS
# ==============================================================================

class Convenio(models.Model):
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Por Vencer', 'Por Vencer'), ('Vencido', 'Vencido')]
    CATEGORIA_CHOICES = [('Hospedaje', 'Hospedaje'), ('Salud', 'Salud'), ('Gastronomía', 'Gastronomía'), ('Deportes', 'Deportes'), ('Educación', 'Educación'), ('Otros', 'Otros')]

    nombre_empresa = models.CharField(max_length=255)
    categoria = models.CharField(max_length=100, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES, default='Activo')
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    contacto_nombre = models.CharField(max_length=255, blank=True)
    contacto_telefono = models.CharField(max_length=20, blank=True)
    contacto_email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    sitio_web = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, related_name='convenios_creados')

    def __str__(self):
        return self.nombre_empresa

class Beneficio(models.Model):
    TIPO_CHOICES = [('Descuento', 'Descuento'), ('Servicio', 'Servicio'), ('Producto', 'Producto'), ('Especial', 'Especial'), ('Otro', 'Otro')]
    
    nombre = models.CharField(max_length=255)
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='beneficios')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.convenio.nombre_empresa})"

class ServicioEspecifico(models.Model):
    beneficio = models.ForeignKey(Beneficio, on_delete=models.CASCADE, related_name='servicios')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def convenio(self):
        return self.beneficio.convenio

    def categoria(self):
        return self.beneficio.convenio.categoria

    def __str__(self):
        return self.nombre

# ==============================================================================
# 4. MODELOS DE CONTENIDO Y OPERACIONES
# ==============================================================================



class Solicitud(models.Model):
    ESTADO_CHOICES = [('Pendiente', 'Pendiente'), ('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')]

    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")
    afiliado = models.ForeignKey(Afiliado, on_delete=models.CASCADE, related_name='solicitudes')
    servicio_especifico = models.ForeignKey(ServicioEspecifico, on_delete=models.CASCADE, related_name='solicitudes', verbose_name="Servicio Específico")
    descripcion = models.TextField(verbose_name="Descripción")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return f"Solicitud #{self.id} - {self.afiliado.razon_social}"

class Reporte(models.Model):
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='reportes/', blank=True, null=True)
    administrador = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Reporte: {self.tipo} ({self.fecha_generacion.strftime('%d/%m/%Y')})"

class Contacto(models.Model):
    ASUNTO_CHOICES = [
        ('afiliacion', 'Información sobre Afiliación'),
        ('certificaciones', 'Certificaciones y Documentos'),
        ('mediacion', 'Centro de Mediación'),
        ('capacitacion', 'Capacitación Empresarial'),
        ('eventos', 'Eventos y Networking'),
        ('servicios', 'Servicios Empresariales'),
        ('comercio_exterior', 'Comercio Exterior'),
        ('otro', 'Otro'),
    ]

    nombre_completo = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    asunto = models.CharField(max_length=30, choices=ASUNTO_CHOICES)
    mensaje = models.TextField()
    acepto_politicas = models.BooleanField(default=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre_completo} ({self.asunto})'
