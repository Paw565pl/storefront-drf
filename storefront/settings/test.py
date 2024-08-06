from .common import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p84^d=98%mj4bvtgo7dn3d38djc*1cfm-!bb9=+@4@1m+xnbz0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

MEDIA_ROOT = BASE_DIR / "media/test"  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "storefront",
        "USER": "postgres",
        "PASSWORD": "mysecretpassword",
        "HOST": "database",
        "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
