import os

from .common import *

from dotenv import load_dotenv

load_dotenv()


DEBUG = os.environ.get('DEBUG')
PRODUCTION = os.environ.get('PRODUCTION')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # noqa
    }
}

SW_CACHE = {
    'host': 'cache',
    'password': os.environ.get('REDIS_PASSWORD'),
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'), # noqa
    os.path.join(BASE_DIR, 'media'), # noqa
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # noqa
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles') # noqa

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'errors.log'),  # Specify your custom log file path
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default'],  # Include your custom handler here
            'level': 'DEBUG',
            'propagate': True,
        },
        'swchars': {
            'handlers': ['file'],  # Include your custom handler here
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
