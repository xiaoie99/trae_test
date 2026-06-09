"""
ASGI config for day06site project.
"""
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'day06site.settings')
application = get_asgi_application()
