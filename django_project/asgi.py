"""
ASGI config for django_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from .secret import DJANGO_ENV

from django.core.asgi import get_asgi_application

if DJANGO_ENV == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_asgi_application()
