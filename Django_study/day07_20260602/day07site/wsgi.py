"""
WSGI config for day07site project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day07site.settings')
application = get_wsgi_application()
