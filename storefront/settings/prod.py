import environ

from .common import *  # noqa

env = environ.Env(LOG_LEVEL=(str, "ERROR"))
environ.Env.read_env(BASE_DIR / ".env")  # noqa: F405

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": env.db(),
}

CELERY_BROKER_URL = env.cache()
CELERY_RESULT_BACKEND = env.cache()

CACHES = {"default": env.cache()}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "general.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "file"], "level": env("LOG_LEVEL")},
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} ({levelname}) - {name} - {message}",
            "style": "{",
        }
    },
}
