from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p84^d=98%mj4bvtgo7dn3d38djc*1cfm-!bb9=+@4@1m+xnbz0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "storefront",
        "USER": "postgres",
        "PASSWORD": "mysecretpassword",
        "HOST": environ.get("DB_HOST", "0.0.0.0"),
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
