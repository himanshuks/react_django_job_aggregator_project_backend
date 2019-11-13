# SECURITY WARNING: don't run with debug turned on in production!
import os
from decouple import config
from decouple import Csv


SECRET_KEY = config('SECRET_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
FILE_UPLOAD_PERMISSIONS = 0o640
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('PGDB_NAME'),
        'USER': config('PGDB_USER'),
        'PASSWORD': config('PGDB_PASSWORD'),
        'HOST': config('PGDB_HOSTS'),
        'PORT': config('PGDB_PORT'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Django rest framework
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
         'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
}
