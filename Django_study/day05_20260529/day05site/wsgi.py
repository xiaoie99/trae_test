"""
WSGI config for day05site project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day05site.settings')
application = get_wsgi_application()
