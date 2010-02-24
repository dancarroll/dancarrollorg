#!/usr/bin/env python

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = ''
SERVER_EMAIL = ''

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'django_db'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

MEDIA_ROOT = '/path/to/media/root/'
MEDIA_URL = '/site-media/'
ADMIN_MEDIA_ROOT = '/path/to/admin-media/root/'
ADMIN_MEDIA_PREFIX = 'http://127.0.0.1:8000/admin-media/'

SECRET_KEY = 'itisasecret'

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

TEMPLATE_DIRS = (
    "/path/to/templates/",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'mysite.blog',
    'tagging',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'debug_toolbar',
)