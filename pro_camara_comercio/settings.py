"""
Django settings for gaoneiz project.
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
    
    # Apps de Terceros (Crispy Forms debe estar aquí)
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
    'allauth.account.middleware.AccountMiddleware',
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

# --- CONFIGURACIÓN DE AUTENTICACIÓN ---
AUTH_USER_MODEL = 'usuarios.Usuario'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuración de django-allauth
SITE_ID = 1
ACCOUNT_EMAIL_VERIFICATION = 'optional' 

# Configuración para usar email en lugar de username
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
# --- FIN DE LA SECCIÓN ---

LOGIN_REDIRECT_URL = 'app_camara_comercio:dashboard'
LOGIN_URL = 'app_camara_comercio:login'
LOGOUT_REDIRECT_URL = 'app_camara_comercio:home'


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