"""
Django settings for lisa_api project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
from lisa_api.lisa.plugin_manager import PluginManager
from lisa_api.lisa.configuration import CONF as config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config.load(filenames=[
    '/etc/lisa/conf/lisa_api.ini',
    BASE_DIR + '/lisa_api.ini',
])

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!k7%j+#7j%=$qsc)b=_m-0fl5f0k-sd7y9olt=cul-q^rcko^3'

# SECURITY WARNING: don't run with debug turned on in production!

config.add_opt(name='debug', value=True, section='api')
DEBUG = config.api.debug

ALLOWED_HOSTS = []

config.add_opt(name='tts', value='google', section='api')
config.add_opt(name='speak', value='rabbitmq', section='api')

# Application definition

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'rest_framework',
    'rest_framework_swagger',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_ENABLED = True

COMPRESS_OFFLINE = True

PROJECT_APPS = [
    'lisa_api.api',
    'lisa_api.frontend',
]

PM = PluginManager()

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS + PluginManager().django_plugins

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'lisa_api.lisa.urls'

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
                'lisa_api.frontend.context_processors.version_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'lisa_api.lisa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

config.add_opt(name='name', value='lisa_api', section='database')
config.add_opt(name='user', value='lisa_api', section='database')
config.add_opt(name='password', value='lisapassword', section='database')
config.add_opt(name='host', value='localhost', section='database')
config.add_opt(name='port', value='3306', section='database')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.database.name,
        'USER': config.database.user,
        'PASSWORD': config.database.password,
        'HOST': config.database.host,
        'PORT': config.database.port,
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

config.add_opt(name='lang_django', value='en-us', section='api')
LANGUAGE_CODE = config.api.lang_django

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING_CONFIG = None

config.add_opt(name='user', value='guest', section='rabbitmq')
config.add_opt(name='password', value='guest', section='rabbitmq')
config.add_opt(name='host', value='localhost', section='rabbitmq')

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
