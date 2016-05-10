from adrian.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['adrian-perm.ru']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}