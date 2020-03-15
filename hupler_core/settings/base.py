"""
Django settings for hupler_core project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from celery.task.schedules import crontab

import braintree
from decouple import config

SECRET_KEY = config('SECRET_KEY')

if config('PRODUCTION') == 'True':
    from .production import *
if config('PRODUCTION') == 'False':
    from .local import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Hupler apps
    'contracts',
    'tenders',
    'hupleruser',
    'payments',
    'bookmarks',
    'socialfeeds',
    'subscriptionplans',
    'recommendations',

    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',
    'knox',
    'djoser',
    'django_filters',
    'rest_framework_filters',
    'social_django',
    'django_countries',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'hupler_core.urls'


# Django social auth
AUTHENTICATION_BACKENDS = [
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'hupleruser.HuplerUser'


# CORS
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)

# DJOSER
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SERIALIZERS': {
        'user': 'hupleruser.serializers.HuplerUserSerializer',
        'current_user': 'hupleruser.serializers.HuplerUserSerializer',
        'user_create_password_retype': 'hupleruser.serializers.DjoserSignUpRePasswordSerializer',
    },
}

# Free plan limiter
FREE_PLAN_LIMIT = 200

# Celery
TIME_ZONE = 'UTC'
USE_TZ = True
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULE = {
    'delete_expired_subscription_plans': {
        'task': 'subscriptionplans.tasks.delete_expired_subscription_plans',
        'schedule': crontab(),
    },
    'update_contracts_database_hourly': {
        'task': 'contracts.tasks.update_contracts_database',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'update_tenders_database_hourly': {
        'task': 'tenders.tasks.update_tenders_database',
        'schedule': crontab(minute=0, hour='*/1'),
    },
    'update_social_feeds_database_hourly': {
        'task': 'socialfeeds.tasks.update_social_feeds_database',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}

# Django Knox
REST_KNOX = {
    'USER_SERIALIZER': 'hupleruser.serializers.HuplerUserSerializer',
}


# Braintree
if config('BRAINTREE_PRODUCTION') == 'False':
    BRAINTREE_ENVIRONMENT = braintree.Environment.Sandbox
if config('BRAINTREE_PRODUCTION') == 'True':
    BRAINTREE_ENVIRONMENT = braintree.Environment.Production

BRAINTREE_MERCHANT_ID = config('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = config('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = config('BRAINTREE_PRIVATE_KEY')

TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

# Social Auth

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = config(
    'SOCIAL_AUTH_FACEBOOK_SECRET')  # App Secret

# SOCIAL_AUTH_INSTAGRAM_KEY = config('SOCIAL_AUTH_INSTAGRAM_KEY')  # App ID
# SOCIAL_AUTH_INSTAGRAM_SECRET = config('SOCIAL_AUTH_INSTAGRAM_SECRET')  # App Secret
# SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [
#     ('user', 'user')
# ]
# SOCIAL_AUTH_INSTAGRAM_REDIRECT_URL = 'http://localhost:8000/complete/instagram'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = config(
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY')  # Client ID
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = config(
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET')  # Client Secret
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    'email-address', 'formatted-name', 'public-profile-url', 'picture-url']
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('formattedName', 'name'),
    ('emailAddress', 'email_address'),
    ('pictureUrl', 'picture_url'),
    ('publicProfileUrl', 'profile_url'),
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hupler_core.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')