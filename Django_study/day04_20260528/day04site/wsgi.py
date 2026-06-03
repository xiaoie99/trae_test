"""
WSGI config for day04site project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day04site.settings')
application = get_wsgi_application()
