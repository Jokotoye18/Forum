"""
Django settings for forum project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config
from decouple import Csv
import django_heroku
import sentry_sdk
import dj_database_url
from sentry_sdk.integrations.django import DjangoIntegration


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'i%3ghwu1qbh(57(j@#mqm9-ql!tv1d_a1hnx&5rz6==!&i8w$!'
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1', cast=Csv())

ENVIRONMENT =config('ENVIRONMENT', default='production')


sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    

    #third party app
    #rest_framework
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    #allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #allauth social
    'allauth.socialaccount.providers.github', 
    'allauth.socialaccount.providers.google',

    #others
    'debug_toolbar',
    'imagekit',
    'django_filters',
    'martor',
    'crispy_forms',
    'admin_honeypot', 
    'storages',
    
    #local app
    'accounts',
    'pages',
    'boards',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',# whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "django.middleware.common.BrokenLinkEmailsMiddleware", #Manager
    'debug_toolbar.middleware.DebugToolbarMiddleware',# debug toolbar
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'forum.urls'

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
                'django.template.context_processors.request',
            ],
        },
    },
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


WSGI_APPLICATION = 'forum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = config('DATABASE_URL')
db_from_env = dj_database_url.config(default=DATABASE_URL, conn_max_age=500, ssl_require=True)
DATABASES['default'].update(db_from_env)


SITE_ID = 1

#Martor
CSRF_COOKIE_HTTPONLY = False
MARTOR_ENABLE_CONFIGS = {
    'emoji': 'true',        # to enable/disable emoji icons.
    'imgur': 'false',        # to enable/disable imgur/custom uploader.
    'mention': 'true',     # to enable/disable mention
    'jquery': 'true',       # to include/revoke jquery (require for admin default django)
    'living': 'true',      # to enable/disable live updates in preview
    'spellcheck': 'false',  # to enable/disable spellcheck in form textareas
    'hljs': 'true',         # to enable/disable hljs highlighting in preview
}

# To setup the martor editor with label or not (default is False)
MARTOR_ENABLE_LABEL = False

import time
# MARTOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
# MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader

# MAX_IMAGE_UPLOAD_SIZE = 2621440  # 2MB

#crispy-form
CRISPY_TEMPLATE_PACK = 'bootstrap4'

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

#debug toolbar
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


#AWS config
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# AWS_REGION = config('AWS_REGION')
# S3_USE_SIGV4 = config('S3_USE_SIGV4', cast=bool)
# print(AWS_ACCESS_KEY_ID, AWS_DEFAULT_ACL, AWS_S3_FILE_OVERWRITE, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_REGION, S3_USE_SIGV4)


# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_S3_SIGNATURE_VERSION = "s3v4"
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_LOCATION = 'static'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }





STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL  = '/'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE =  True 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True 
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED  = True
ACCOUNT_UNIQUE_USERNAME = True 


# if DEBUG:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

DEFAULT_FROM_EMAIL = 'Forum <jokotoyeademola995@gmail.com>'

SERVER_EMAIL = DEFAULT_FROM_EMAIL

MANAGER = (
    ('Jokotoye Ademola', 'jokotoyeademola995@gmail.com'),
)

ADMIN = MANAGER




if ENVIRONMENT == 'production':
    CACHE = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache', 
            'LOCATION': '127.0.0.1:11211',
            'OPTIONS': {
                'server_max_value_length': 1024 * 1024 * 2,
            }
        }
    }
    

    #HTTP Strict Transport Security (HSTS)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_PRELOAD = True

    #Cross-Site Request Forgery (CSRF)
    CSRF_COOKIE_SECURE = True  # cookie will only be sent over an HTTPS connection

    
    # SECURE_REFERRER_POLICY = 'same-origin'
    
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    #Cross-Site Scripting (XSS)
    SECURE_BROWSER_XSS_FILTER = True
    SESSION_COOKIE_HTTPONLY = True
    #django-csp(Details at official docs)

django_heroku.settings(locals())

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS':	(
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    )	
} 