from .base import *  # noqa
from os import environ
import djcelery
import raven


# Disable debug mode

DEBUG = False
TEMPLATE_DEBUG = False


# Compress static files offline
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE

COMPRESS_OFFLINE = True


# Send notification emails as a background task using Celery,
# to prevent this from blocking web server threads
# (requires the django-celery package):
# http://celery.readthedocs.org/en/latest/configuration.html


djcelery.setup_loader()

CELERY_SEND_TASK_ERROR_EMAILS = True
BROKER_URL = environ.get("BROKEN_URL")


# Use Redis as the cache backend for extra performance
# (requires the django-redis-cache package):
# http://wagtail.readthedocs.org/en/latest/howto/performance.html#cache

# CACHES = {
#     "default": {
#         "BACKEND": "redis_cache.cache.RedisCache",
#         "LOCATION": "127.0.0.1:6379",
#         "KEY_PREFIX": "base",
#         "OPTIONS": {
#             "CLIENT_CLASS": "redis_cache.client.DefaultClient",
#         }
#     }
# }

RAVEN_CONFIG = {
    'dsn': environ.get('RAVEN_DSN'),
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(__file__)),
}

# Setup for CAS
ENABLE_SSO = True

MIDDLEWARE_CLASSES += [
    "molo.core.middleware.MoloCASMiddleware",
    "molo.core.middleware.Custom403Middleware",
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "molo.core.backends.MoloCASBackend",
]

CAS_SERVER_URL = ""
CAS_ADMIN_PREFIX = "/admin/"
LOGIN_URL = "/accounts/login/"
CAS_VERSION = "3"

try:
    from .local import *  # noqa
except ImportError:
    pass
