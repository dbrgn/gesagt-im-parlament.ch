# coding=utf-8
# Django settings for deployment on ep.io

from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'dbrgn_parlament',       # Or path to database file if using sqlite3.
    'USER': 'dbrgn_parlament',       # Not used with sqlite3.
    'PASSWORD': '',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}

INSTALLED_APPS = (
    # Contrib apps
    'django.contrib.staticfiles',

    # Own apps
    'apps.front',

    # 3rd party apps
    'gunicorn',
)

STATIC_ROOT = '/home/dbrgn/webapps/static/'
