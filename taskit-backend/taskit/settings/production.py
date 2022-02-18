import dj_database_url
from taskit.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["taskitbackend.herokuapp.com"]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 1

SECURE_SSL_REDIRECT = True

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {}
DATABASES["default"] = dj_database_url.config(conn_max_age=600)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


# django-cors-headers settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
