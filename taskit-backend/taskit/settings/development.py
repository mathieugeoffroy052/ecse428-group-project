from taskit.settings.common import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(^glqg@qq&3f+g0=16mw2ldlp=9d9)g#gv56v3xnul(sob^0h4"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# django-cors-headers settings
CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "https://taskitfrontend.herokuapp.com"]
