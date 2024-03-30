from os import environ

from .common import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p84^d=98%mj4bvtgo7dn3d38djc*1cfm-!bb9=+@4@1m+xnbz0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

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
