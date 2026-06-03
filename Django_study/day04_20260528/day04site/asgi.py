"""
ASGI config for day04site project.
"""
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day04site.settings')
application = get_asgi_application()
