"""
ASGI config for day08site project.
"""
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day08site.settings')
application = get_asgi_application()
