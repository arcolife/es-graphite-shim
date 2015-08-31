#!/usr/bin/env python3
"""
Django settings for egs project
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

SECRET_KEY = "$dfct5s9)*)+kt*9=jiosd714c52d4-e64c-9c42-b6724f7b6f6"


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': None,
    }
}
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

from local_settings import cache, ES

import socket
hostname = socket.gethostname()
del socket

# SECURITY WARNING: don't run with debug turned on in production!
if hostname == cache.get('HOSTNAME'):
    DEBUG = False
    PRODUCTION = True
else:
    # All other environments are assumed to be non-production
    # environments. You can override this settings here to test out production
    # like behaviors.
    DEBUG = True
    PRODUCTION = False

TEMPLATE_DEBUG = True

# FIXME: If you want to test development mode with ./manage.py runserver as if
# it would be production, you need to add 'localhost' or '*' to the
# ALLOWED_HOSTS list, set DEBUG above to False, and you need to use the
# --insecure switch on runserver (e.g. $ python3 ./manage.py runserver
# --insecure).

if DEBUG:
    ALLOWED_HOSTS = ['']
elif PRODUCTION:
    # ALLOWED_HOSTS = [HOSTNAME,]
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['localhost',]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'egs.urls'
WSGI_APPLICATION = 'egs.wsgi.application'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {}
# DATABASES = {
#     'default': {
#         'NAME': os.path.join(BASE_DIR, 'storage/%s.sqlite3' % (DB_NAME)),
#         'ENGINE': 'django.db.backends.sqlite3',
#         'USER': 'apache',
#         'PASSWORD': DB_PASS,
#         'HOST': '',
#         'PORT': ''
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# FIXME: either remove, or configure based on local settings

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = '/mnt/static'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates/'),)

# django log setup.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            # 'filename': os.path.join(BASE_DIR, 'django.log'),
            'filename': '/opt/egs/logs/django.log',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'logfile']
    },
}
