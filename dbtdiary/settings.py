import os
import sys
import platform

import djcelery

djcelery.setup_loader()

from django.contrib.messages import constants as messages

# ===========================
# = Directory Declaractions =
# ===========================

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR   = os.path.dirname(__file__)
TEMPLATE_DIRS = (os.path.join(CURRENT_DIR, 'templates'),)
UTILS_ROOT    = os.path.join(CURRENT_DIR, 'utils')
APPS_ROOT   = os.path.join(CURRENT_DIR, 'apps')

if '/utils' not in ' '.join(sys.path):
    sys.path.append(UTILS_ROOT)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (('Marie VerMurlen', 'marie@violetco.de'))
MANAGERS = ADMINS

#DB info injected by Heroku
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

#Global Settings

TIME_ZONE = 'America/Los_Angeles'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ALLOW_NEW_REGISTRATIONS = True
PUBLIC = True

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 30

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(SITE_ROOT, 'static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()

WSGI_APPLICATION = 'dbtdiary.wsgi.application'

AUTH_PROFILE_MODULE = "dbtdiary.diary.UserProfile"

# ===========================
# = Django-specific Modules =
# ===========================

SECRET_KEY = 'wzqxrx6a7a=2a^ubw$_a_ozah+cvtslmx81f$8ecfdmgk=wtty'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)


ROOT_URLCONF = 'dbtdiary.urls'

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (

	#Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',

    #Prancing on Heroku
    'gunicorn',
    'south',
    'djcelery',

    #Internal
    'dbtdiary.diary',
    'dbtdiary.accounts',
    
)