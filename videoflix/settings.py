"""
Django settings for videoflix project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8hi_#n)tx8ymiwq9i)l9ca&ei2z!zd3xszvz!%mn44nypn$p+y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
		    'localhost',
		    '127.0.0.1',
            'leonard-weiss.developerakademie.org'
		]
CORS_ALLOWED_ORIGINS = [
		    'http://localhost:4200',
		    'http://localhost:8000',
		    'http://127.0.0.1:8000',
		    'http://127.0.0.1:4200',
            'https://leonard-weiss.developerakademie.net/'
            'http://leonard-weiss.developerakademie.org',
            'https://leonard-weiss.developerakademie.org',
            
]

CSRF_TRUSTED_ORIGINS = [
    'https://leonard-weiss.developerakademie.org',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'debug_toolbar',
    'django_rq',
    'userAuthentication.apps.UserauthenticationConfig',
    'content.apps.ContentConfig',
    'imagekit',
    'corsheaders',
]

# Define custom user model
AUTH_USER_MODEL = 'userAuthentication.CustomUser'

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'videoflix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'videoflix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'live.smtp.mailtrap.io'
EMAIL_HOST_USER = 'api'
EMAIL_HOST_PASSWORD = '88f0a49d8a2d7c6c9d82ed73f17b04fb'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

#static files und templats
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

# Redis config
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "PASSWORD": "foobared",
        },
        "KEY_PREFIX": "videoflix"
    }
}

CACHE_TTL = 60 * 15 # Cach total life time: 15 minutes

# Django Toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# Config of RQ
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'foobared',
        'DEFAULT_TIMEOUT': 360,
    },
}

# App Base URL
#FRONTEND_BASE_URL = "http://localhost:4200"
FRONTEND_BASE_URL = "https://leonard-weiss.developerakademie.net//angular-projects/videoflix/"
BACKEND_BASE_URL = 'https://leonard-weiss.developerakademie.org/videoflix/v1'
