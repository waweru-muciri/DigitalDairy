"""
Django settings for LearningDjango project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import django_heroku
from corsheaders.defaults import default_headers
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$=jxc++jhcmbubxpy9pvet@=(b9@9usb*ms#s-qwkiecjg$z7)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    'digitaldairy.apps.DigitaldairyConfig',
    'digitalDairyApi.apps.DigitaldairyapiConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'mathfilters',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_registration',
    'fcm_django',
]

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAMs4p04M:APA91bHc6njCwxoPoBZX_E7CqTm7cZvB9BmMjcs8i9vvHqqvZS5KejICtbAYZ5ljzXzdGLklsSu7DfvQnnv_LuC-rZ0dNkV3RaD7e66p4MXbCvGrGkw3-czgn4gRlpD3WqlaxIoakfU3",
    "APP_VERBOSE_NAME": "digitaldairy",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'LearningDjango.middleware.ServiceWorkerMiddleware',
]

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

ROOT_URLCONF = 'LearningDjango.urls'

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

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-CSRFTOKEN',
]
CORS_ORIGIN_ALLOW_ALL = True

WSGI_APPLICATION = 'LearningDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DigitalDairy',
                'USER': 'brian',
                'PASSWORD': 'admin',
                'HOST': '127.0.0.1',
                'ssl_disabled': 'True',
    },
    # 'event_company': {
    # 		'ENGINE': 'django.db.backends.postgresql',
    # 		'NAME': 'eventcompany',
    # 		'USER': 'brian',
    # 		'PASSWORD': 'admin',
    # 		'HOST': '127.0.0.1',
    # 		'ssl_disabled' : 'True',
    # 	}
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DATABASE_ROUTERS = ['LearningDjango.DbRouter.DbRouter']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'brianmuciri@digitaldairy.services'
EMAIL_HOST_PASSWORD = 'spb!b!@gQNV@#q9'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

#STATIC_URL = '/digitaldairy/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "digitaldairy/templates/digitaldairy"),
    os.path.join(BASE_DIR, "digitaldairy/templates/accounts"),
]
# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/digitaldairy/daily_milk_production/'
ACCOUNT_ACTIVATION_DAYS = 7  # one week activation window
# if DEBUG:
#     EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
# ]
django_heroku.settings(locals())
