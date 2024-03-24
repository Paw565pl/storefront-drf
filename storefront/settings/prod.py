# from os import environ
#
# from dj_database_url import config as db_config
#
# SECRET_KEY = environ["SECRET_KEY"]
#
# DEBUG = False
#
# ALLOWED_HOSTS = []
#
# DATABASES = {"default": db_config()}
#
# REDIS_URL = environ.get("REDIS_URL")
#
# CELERY_BROKER_URL = REDIS_URL
#
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": REDIS_URL,
#         "TIMEOUT": 10 * 60,
#     }
# }
#
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "class": "logging.FileHandler",
#             "filename": "general.log",
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console", "file"],
#             "level": environ.get("DJANGO_LOG_LEVEL", "INFO"),
#         },
#     },
#     "formatters": {
#         "verbose": {
#             "format": "{asctime} ({levelname}) - {name} - {message}",
#             "style": "{",
#         }
#     },
# }
