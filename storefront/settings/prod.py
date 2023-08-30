from os import environ
from .common import *
from dj_database_url import config as db_config

SECRET_KEY = environ["SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {"default": db_config()}

REDIS_URL = environ.get("REDIS_URL")

CELERY_BROKER_URL = REDIS_URL

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "TIMEOUT": 10 * 60,
    }
}
