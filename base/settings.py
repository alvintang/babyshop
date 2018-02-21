# -*- coding: utf-8 -*-
"""
Django settings
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, sys
#import django
#django.setup()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vqje&(s$kn!osyitq#y%y1)g7-63#ia#+45(d&c%7x7u)d!pn3'

# SECURITY WARNING: don't run with debug turned on in production!

# PYTHON version
PYTHON_VERSION = sys.version_info

#TESTING = sys.argv[1:2] == ['test']
#if TESTING:
DEBUG = True
#else:
#    DEBUG = True

DEBUG_PROPAGATE_EXCEPTIONS = True
#DEBUG = DEBUG_PROPAGATE_EXCEPTIONS

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    # 'django_admin_bootstrapped',
    'babysetgo',
    'base',
    'users',
    'cachalot',
    'debug_toolbar',
    'material',
    'material.admin',
    'material.frontend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django_countries',
    'cookielaw',
    'django_extensions',
    'registry',
    'crispy_forms',
    'sslserver',
    'djangosecure',
    'carton',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'registry.middleware.AutoClearCart',
)

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': ['../templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'base.context_processors.breadcrumbs',
                'base.context_processors.add_login_form'
            ],
            'debug': DEBUG,
        },
    },
]
# WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'babysetgo',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '8889',
     }

    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}

# Cache: http://django-cachalot.readthedocs.io/en/latest/quickstart.html
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHALOT_ENABLED = True
CACHALOT_CACHE = 'default'

# Django toolbar https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'cachalot.panels.CachalotPanel',
]


def show_toolbar(request):
    return DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LOCALE_PATHS = [
    # '/django-app/locale',
    os.path.join(BASE_DIR, 'locale')
]

AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'base.validators.CustomPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-es'

LANGUAGES = (
    ('es', 'Espanol (Espana)'),
    ('en', 'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
#STATIC_URL = '//babysetgo.ph/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'base/static/')
#STATIC_ROOT = '/home/alvintang/webapps/static/' 

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

LOGIN_URL = '/'


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
FIXTURE_DIRS = ('babysetgo/fixtures',)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Django registration

# To indicate if the register its open.
REGISTRATION_OPEN = True
# https://django-registration.readthedocs.io/en/2.1.1/settings.html#django.conf.settings.REGISTRATION_OPEN


# Configuring the HMAC activation workflow

# To specify the days that the user must be activate his register.
ACCOUNT_ACTIVATION_DAYS = 1
# https://django-registration.readthedocs.io/en/2.1.1/settings.html#django.conf.settings.ACCOUNT_ACTIVATION_DAYS

# To specify a str to construct the activation code
REGISTRATION_SALT = 'registration'
# https://django-registration.readthedocs.io/en/2.1.1/settings.html#django.conf.settings.REGISTRATION_SALT

# Email config
DEFAULT_FROM_EMAIL = 'info@babysetgo.ph'
EMAIL_TO = 'info@babysetgo.ph'

ADMINS = (('Alvin', 'alvin@babysetgo.ph'), ('Issa','issa@babysetgo.ph'))

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'babysetgo_issa'
EMAIL_HOST_PASSWORD = 'Ts0k0leyt!'
SERVER_EMAIL = 'info@babysetgo.ph'
EMAIL_PORT = 587

# django-carton variables
CART_PRODUCT_MODEL = 'registry.models.RegistryItem'
CART_SESSION_KEY = 'cart_session'
AUTO_CLEARCART_DELAY = 15 # in minutes

# for middleware serializer
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# for partner stores
PARTNER_STORES = [
    'https://funnest.ph/',
    'funnest.ph',
    'http://www.stpatrickbaby.com/',
    'stpatrickbaby.com',
    'http://www.mightybaby.ph/',
    'mightybaby.ph',
]

PRICE_REF = [1500,3000,5000]
DELIVERY_FEE_REF = [150,300,500,750]
DELIVERY_FEE_REF_PARTNER_STOR = [150,300,500,750]