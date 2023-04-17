from .settings import *
import os

SECRET_KEY = os.environ.get('SECRET_KEY')

SECRET_KEY_FALLBACKS = ['&@-o*pb+_$x+gclovr4v98-(+-*@ey0yi+7qm(2g8i5#p6zt@8']

DEBUG = False

ALLOWED_HOSTS = ['studentsinfo.me', '127.0.0.1', '20.205.119.69']

CSRF_TRUSTED_ORIGINS = [
    'http://.*',
    'https://studentsinfo.me',
    'https://20.205.119.69',
    'http://127.0.0.1',
]

STATICFILES_DIRS = [
    BASE_DIR / 'students/static',
    '/home/meraj/staticfiles',
]
