"""
Django settings for pro_camara_comercio project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = 'django-insecure-uz3ql(3+5!n!e!zmpgct#m^pniywg=50_2grb8*90o$ozxof1j'
DEBUG = True
ALLOWED_HOSTS = []

# --- APLICACIONES (INSTALLED_APPS) ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Mis Aplicaciones
    'usuarios.apps.UsuariosConfig',
    'web.apps.WebConfig',
    'noticias.apps.NoticiasConfig',
    'convenios.apps.ConveniosConfig',
    'servicios.apps.ServiciosConfig',
    'afiliaciones.apps.AfiliacionesConfig',
    'panel.apps.PanelConfig',
    'reservas.apps.ReservasConfig',
    
    # Apps de Terceros
    'crispy_forms',
    'crispy_bootstrap5',
    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # Middleware de Allauth
]

ROOT_URLCONF = 'pro_camara_comercio.urls'

# --- PLANTILLAS (TEMPLATES) ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pro_camara_comercio.wsgi.application'

# --- BASE DE DATOS (DATABASE) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- CONFIGURACIÓN DE AUTENTICACIÓN Y DJANGO-ALLAUTH ---

# Modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'

# Backends de autenticación (necesario para allauth)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# ID del sitio para allauth
SITE_ID = 1

# Configuraciones principales de Allauth (versión actualizada)
ACCOUNT_LOGIN_METHODS = ['email']       # Se usará el email para iniciar sesión.
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Verificación de correo obligatoria.
ACCOUNT_LOGOUT_ON_GET = True              # Permite cerrar sesión con una petición GET.
ACCOUNT_EMAIL_REQUIRED = True             # El email es requerido para registrarse.
ACCOUNT_UNIQUE_EMAIL = True               # Asegura que los correos sean únicos.
ACCOUNT_USERNAME_REQUIRED = False         # El nombre de usuario no es requerido.
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # Indica que no hay campo de username en el modelo.
ACCOUNT_AUTHENTICATION_METHOD = 'email'   # Método de autenticación es el email.

# Formulario de registro personalizado
ACCOUNT_FORMS = {
    'signup': 'usuarios.forms.CustomSignupForm',
}

# Redirecciones después de login/logout
LOGIN_REDIRECT_URL = 'web:home'
LOGIN_URL = 'account_login'
LOGOUT_REDIRECT_URL = 'web:home'

# Backend de correo para desarrollo (imprime emails en la consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- ARCHIVOS ESTÁTICOS Y MEDIA ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- CONFIGURACIONES DE TERCEROS (CRISPY FORMS) ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --- LLAVE PRIMARIA POR DEFECTO ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guayaquil'
USE_L10N = True
USE_TZ = True