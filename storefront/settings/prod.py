import environ

from .common import *  # noqa

env = environ.Env(
    CELERY_BROKER_URL=str, CELERY_RESULT_BACKEND_URL=str, LOG_LEVEL=(str, "ERROR")
)
environ.Env.read_env(BASE_DIR / ".env")  # noqa: F405

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "backend"]

DATABASES = {
    "default": env.db(),
}

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND_URL")

CACHES = {"default": env.cache()}

EMAIL_CONFIG = env.email()
vars().update(EMAIL_CONFIG)

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
