"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from .secret import DJANGO_ENV

from django.core.wsgi import get_wsgi_application

if DJANGO_ENV == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

application = get_wsgi_application()
