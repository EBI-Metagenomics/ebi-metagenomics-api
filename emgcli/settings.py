#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2017 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Django settings for emg project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import sys
import os
import warnings
import logging
import binascii
import datetime

from os.path import expanduser

try:
    from YamJam import yamjam, YAMLError
except ImportError:
    raise ImportError("Install yamjam. Run `pip install -r requirements.txt`")

logger = logging.getLogger(__name__)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMG_CONFIG = os.environ.get(
    'EMG_CONFIG', os.path.join(expanduser("~"), 'emg', 'config.yaml')
)
EMG_CONF = yamjam(EMG_CONFIG)


try:
    LOGDIR = EMG_CONF['emg']['log_dir']
except KeyError:
    LOGDIR = os.path.join(expanduser("~"), 'emg', 'log')
if not os.path.exists(LOGDIR):
    os.makedirs(LOGDIR)

LOGGING_CLASS = 'cloghandler.ConcurrentRotatingFileHandler'
LOGGING_FORMATER = (
    '%(asctime)s %(levelname)5.5s [%(name)30.30s]'
    ' (proc.%(process)5.5d) %(funcName)s:%(lineno)d %(message)s')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'default': {
            'format': LOGGING_FORMATER
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': LOGGING_CLASS,
            'filename': os.path.join(LOGDIR, 'emg.log').replace('\\', '/'),
            'maxBytes': 1024*1024*10,
            'backupCount': 50,
            'formatter': 'default',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'default',
        },
    },
    'loggers': {
        'django.request': {  # Stop SQL debug from logging to main logger
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': True
        },
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

def create_secret_key(var_dir):
    secret_key = None
    dir_fd = os.open(var_dir, os.O_RDONLY)

    key_path = os.path.join(var_dir, 'secret.key')
    if not os.path.exists(key_path):
        with os.fdopen(os.open(key_path,
                               os.O_WRONLY | os.O_CREAT,
                               0o600), 'w') as f:  # noqa
            f.write(binascii.hexlify(os.urandom(50)).decode('ascii'))
    with open(key_path, 'r') as f:
        secret_key = f.read().rstrip()
    os.close(dir_fd)
    return secret_key

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY_DIR = EMG_CONF['emg']['secret_key']
except KeyError:
    SECRET_KEY_DIR = os.path.join(expanduser("~"), 'emg')

try:
    SECRET_KEY
except NameError:
    SECRET_KEY = create_secret_key(SECRET_KEY_DIR)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # CORS
    'corsheaders',
    # UI
    'emgui',
    # rest framework
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_mongoengine',
    'rest_framework_jwt',
    'django_filters',
    # apps
    'emgapi',
    'emgena',
    'emgapianns',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Django CORS middleware
    'corsheaders.middleware.CorsMiddleware',
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ETAGS support
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emgcli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'emgcli.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(EMG_DIR, 'db.sqlite3'),
#     }
# }
try:
    DATABASES = EMG_CONF['emg']['databases']
except KeyError:
    raise KeyError("Config must container default database.")

try:
    SESSION_ENGINE = EMG_CONF['emg']['session_engine']
except KeyError:
    pass

try:
    CACHES = EMG_CONF['emg']['caches']
except KeyError:
    pass

try:
    CONN_MAX_AGE = EMG_CONF['emg']['conn_max_age']
except KeyError:
    pass


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Django Rest Framewrk

REST_FRAMEWORK = {

    'DEFAULT_VERSIONING_CLASS':
        'rest_framework.versioning.NamespaceVersioning',

    'DEFAULT_VERSION': '1',

    'PAGE_SIZE': 25,

    'EXCEPTION_HANDLER':
        'rest_framework_json_api.exceptions.exception_handler',

    'DEFAULT_PAGINATION_CLASS':
        # 'rest_framework.pagination.PageNumberPagination',
        'emgcli.pagination.DefaultPagination',

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
        # 'rest_framework_xml.parsers.XMLParser',
        # 'rest_framework_yaml.parsers.YAMLParser',
        # 'rest_framework.parsers.MultiPartParser'
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'emgapi.renderers.DefaultJSONRenderer',
        # 'rest_framework.renderers.JSONRenderer',
        'emgapi.renderers.JSONLDRenderer',
        # 'rest_framework_xml.renderers.XMLRenderer',
        # 'rest_framework_yaml.renderers.YAMLRenderer',
        'emgapi.renderers.CSVStreamingRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_METADATA_CLASS':
        'rest_framework_json_api.metadata.JSONAPIMetadata',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
   ],

}

JSON_API_FORMAT_KEYS = 'dasherize'
JSON_API_FORMAT_TYPES = 'dasherize'
JSON_API_PLURALIZE_TYPES = True

# Swagger auth
# Toggles the use of Django Auth as an authentication mechanism.
# Note: The login/logout button relies on the LOGIN_URL and LOGOUT_URL
# settings These can either be configured under SWAGGER_SETTINGS or Django settings.
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

# Custom settings
try:
    EMG_DEFAULT_LIMIT = REST_FRAMEWORK['PAGE_SIZE']
except:
    EMG_DEFAULT_LIMIT = 20

# Authentication backends
try:
    AUTHENTICATION_BACKENDS = EMG_CONF['emg']['auth_backends']
except:
    AUTHENTICATION_BACKENDS = (
        'emgapi.backends.EMGBackend',
    )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
try:
    FORCE_SCRIPT_NAME = EMG_CONF['emg']['prefix'].rstrip('/')
    if not FORCE_SCRIPT_NAME.startswith("/"):
        FORCE_SCRIPT_NAME = "/%s" % FORCE_SCRIPT_NAME
except KeyError:
    FORCE_SCRIPT_NAME = ''


try:
    STATIC_ROOT = EMG_CONF['emg']['static_root']
except KeyError:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WHITENOISE_STATIC_PREFIX = '/static/'

STATIC_URL = '%s%s' % (FORCE_SCRIPT_NAME, WHITENOISE_STATIC_PREFIX)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Security
try:
    secure_cookies = EMG_CONF['emg']['secure_cookies']
except KeyError:
    secure_cookies = True

try:
    SECURE_PROXY_SSL_HEADER = EMG_CONF['emg']['secure_proxy_ssl_header']
except KeyError:
    SECURE_PROXY_SSL_HEADER = None

X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_SECURE = secure_cookies
SESSION_COOKIE_SECURE = secure_cookies
SECURE_CONTENT_TYPE_NOSNIFF = True

try:
    ALLOWED_HOSTS = EMG_CONF['emg']['allowed_host']
    CORS_ORIGIN_WHITELIST = ALLOWED_HOSTS
    logger.info("ALLOWED_HOSTS %r" % CORS_ORIGIN_WHITELIST)
except KeyError:
    warnings.warn("ALLOWED_HOSTS not configured using wildecard",
                  RuntimeWarning)

CORS_ORIGIN_ALLOW_ALL = False
# CORS_URLS_REGEX = r'^%s/.*$' % FORCE_SCRIPT_NAME
# CORS_URLS_ALLOW_ALL_REGEX = ()
CORS_ALLOW_METHODS = (
    'GET',
    'HEAD',
    'OPTIONS',
)

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=108000),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

try:
    ADMINS = EMG_CONF['emg']['admins']
    MANAGERS = ADMINS
    # IGNORABLE_404_URLS
except KeyError:
    ADMINS = []
    warnings.warn("ADMINS not configured, no error notification",
                  RuntimeWarning)

# EMAIL
try:
    EMAIL_HOST = EMG_CONF['emg']['email']['host']
    EMAIL_PORT = EMG_CONF['emg']['email']['port']
    EMAIL_SUBJECT_PREFIX = EMG_CONF['emg']['email']['subject']
    MIDDLEWARE += ('django.middleware.common.BrokenLinkEmailsMiddleware',)

    LOGGING['handlers']['mail_admins'] = \
        {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    if 'mail_admins' not in LOGGING['loggers']['django.request']['handlers']:
        LOGGING['loggers']['django.request']['handlers'].append('mail_admins')
except KeyError:
    warnings.warn(
        "EMAIL not configured, no error notification for %r." % ADMINS,
        RuntimeWarning
    )

try:
    EMAIL_HELPDESK = EMG_CONF['emg']['email']['helpdesk']
except KeyError:
    warnings.warn(
        "Helpdesk notificationnot provided", RuntimeWarning
    )

try:
    RT = EMG_CONF['emg']['rt']
except KeyError:
    warnings.warn("RT not configured.", RuntimeWarning)

# SLACK
try:
    SLACK_TOKEN = EMG_CONF['emg']['slack']['token']
    SLACK_CHANNEL = EMG_CONF['emg']['slack']['channel']
    SLACK_USERNAME = EMG_CONF['emg']['slack']['username']
    SLACK_FAIL_SILENTLY = EMG_CONF['emg']['slack']['fail_silently']
    SLACK_BACKEND = 'django_slack.backends.RequestsBackend'
    INSTALLED_APPS += ('django_slack',)
    MIDDLEWARE += ('emgcli.middleware.BrokenLinkSlackMiddleware',)

    LOGGING['handlers']['slack_admins'] = \
    {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django_slack.log.SlackExceptionHandler',
    }
    if 'slack_admins' not in LOGGING['loggers']['django.request']['handlers']:
        LOGGING['loggers']['django.request']['handlers'].append('slack_admins')
except KeyError:
    warnings.warn("SLACK not configured.", RuntimeWarning)

# EMG
try:
    EMG_BACKEND_AUTH_URL = EMG_CONF['emg']['emg_backend_auth']
except KeyError:
    EMG_BACKEND_AUTH_URL = None

# Documentation
try:
    EMG_TITLE = EMG_CONF['emg']['documentation']['title']
except KeyError:
    EMG_TITLE = 'MGnify API'
try:
    EMG_URL = EMG_CONF['emg']['documentation']['url']
except KeyError:
    EMG_URL = FORCE_SCRIPT_NAME
try:
    EMG_DESC = EMG_CONF['emg']['documentation']['description']
except KeyError:
    EMG_DESC = 'MGnify API'

# MongoDB
import mongoengine

mongodb = EMG_CONF['emg']['mongodb']
MONGO_CONN = mongoengine.connect(**mongodb)


# TODO: fix warnings
SILENCED_SYSTEM_CHECKS = ["fields.W342"]

try:
    TOP10BIOMES = EMG_CONF['emg']['ui']['biomes']
except KeyError:
    TOP10BIOMES = {
        85: 'root:Environmental:Aquatic',
        132: 'root:Environmental:Aquatic:Marine',
        220: 'root:Environmental:Terrestrial:Soil',
        353: 'root:Host-associated:Human',
        356: 'root:Host-associated:Human:Digestive system',
        401: 'root:Host-associated:Human:Skin',
        421: 'root:Host-associated:Mammals:Digestive system',
        466: 'root:Host-associated:Plants',
        62: 'root:Engineered:Wastewater',
        31: 'root:Engineered:Food production',
    }

try:
    RESULTS_DIR = EMG_CONF['emg']['results_dir']
except KeyError:
    RESULTS_DIR = os.path.join(expanduser("~"), 'results')
