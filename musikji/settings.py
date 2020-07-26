"""
Django settings for musikji project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hl*n_c5lmwd7@3!)j2%yv70eh%=zea09i+3%mod$d&hz_n^xji'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['161.35.75.55','muzikji.com',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'archive',
    'backoffice',
    'users.apps.UsersConfig',
    'crispy_forms',
    'django_summernote',
    'django_countries',
    'directmessages',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'musikji.urls'

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

WSGI_APPLICATION = 'musikji.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG == True:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'test1',
			'USER': 'postgres',
			'PASSWORD': 'pic16F877',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}
else:
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'prod',
			'USER': 'u_prod',
			'PASSWORD': '123',
			'HOST': 'localhost',
			'PORT': '5432',
		}
	}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'archive:archive_home'
LOGIN_URL = "login"

#setting for summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'

SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,
        'width': '100%',
        'height': '150',
        'toolbar': ['bold', 'italic', 'underline'],
    },
    'disable_attachment': True,
}

# settings for messages
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

DOWNLOAD_SCORE_POINTS = 5
RATING_MEDIAN = 2.5

DEFAULT_FROM_EMAIL = "Mazen from musikji.tn"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_PASSWORD = 'DSE_Power2'  
EMAIL_HOST_USER = 'slachist@gmail.com'
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER