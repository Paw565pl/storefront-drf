from os import environ

from .common import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p84^d=98%mj4bvtgo7dn3d38djc*1cfm-!bb9=+@4@1m+xnbz0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda request: True,
# }
#
# INSTALLED_APPS.append("debug_toolbar")
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
#
# INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "storefront",
        "USER": "postgres",
        "PASSWORD": "mysecretpassword",
        "HOST": environ.get("DB_HOST", "localhost"),
        "PORT": "5432",
    }
}

CELERY_BROKER_URL = "redis://redis:6379"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
        "TIMEOUT": 10 * 60,
    }
}
