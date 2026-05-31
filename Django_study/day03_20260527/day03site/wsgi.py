"""
WSGI config for day03site project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day03site.settings')
application = get_wsgi_application()
