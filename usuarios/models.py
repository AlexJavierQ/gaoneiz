# usuarios/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

class UsuarioManager(UserManager):
    """Manager personalizado para el modelo Usuario."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario con el email y contraseña dados."""
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario con el email y contraseña dados."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    """
    Modelo de usuario principal y unificado. Hereda de AbstractUser de Django.
    """
    # Se elimina el campo 'username' tradicional para usar el email como identificador único.
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Campos adicionales para todos los usuarios.
    cedula = models.CharField(max_length=20, unique=True, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    # Se configura el email como el campo para iniciar sesión.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Usar el manager personalizado
    objects = UsuarioManager()

    def __str__(self):
        return self.get_full_name() or self.email

    @property
    def es_socio(self):
        """Propiedad que verifica si el usuario tiene un perfil de socio activo."""
        return hasattr(self, 'perfil_socio') and self.perfil_socio.is_active

    @property
    def es_admin(self):
        """Propiedad para verificar si el usuario es parte del personal."""
        return self.is_staff

class PerfilSocio(models.Model):
    """
    Este modelo contiene la información EXTRA que solo pertenece a los socios.
    Está vinculado al modelo Usuario a través de una relación One-to-One.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_socio')
    
    TIPO_PLAN_CHOICES = [
        ('NATURAL', 'Persona Natural'),
        ('EMPRESA', 'Empresa'),
        ('FINANCIERO', 'Entidad Financiera'),
    ]
    
    razon_social = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13, unique=True, verbose_name="RUC")
    direccion = models.TextField()
    tipo_plan = models.CharField(max_length=20, choices=TIPO_PLAN_CHOICES)
    is_active = models.BooleanField(default=False, help_text="Indica si la afiliación del socio está activa.")
    fecha_afiliacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razon_social