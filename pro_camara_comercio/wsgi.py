# pro_camera_comercio/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro_camera_comercio.settings')

application = get_wsgi_application()