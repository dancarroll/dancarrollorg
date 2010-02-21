# Django settings for mysite project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Dan Carroll', 'dancarroll@gmail.com'),
)

MANAGERS = ADMINS

# These should be defined in the local_settings.py file
#EMAIL_HOST = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_HOST_USER = ''
#EMAIL_PORT = ''
#SERVER_EMAIL = ''

# These should be defined in the local_settings.py file
#DATABASE_ENGINE = ''
#DATABASE_NAME = ''
#DATABASE_USER = ''
#DATABASE_PASSWORD = ''
#DATABASE_HOST = ''
#DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/erunama/media.erunama.com/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.erunama.com/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
# This should be defined in the local_settings.py file
# SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware', # will add this to local_settings.py
)

ROOT_URLCONF = 'mysite.urls'

# This should be defined in the local_settings.py file
#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    ""
#)

# Overrides the default in order to remove I18N processor
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'mysite.polls',
    'mysite.blog',
    'tagging',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'debug_toolbar', # will add this to local_settings.py if needed
)

try:
    from local_settings import *
except ImportError:
    pass
