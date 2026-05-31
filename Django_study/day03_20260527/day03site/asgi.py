"""
ASGI config for day03site project.
"""
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day03site.settings')
application = get_asgi_application()
