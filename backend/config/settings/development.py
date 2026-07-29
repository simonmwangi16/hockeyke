"""Local development settings with safe, overridable defaults."""

import os

from .base import *  # noqa: F403
from .base import env_bool, env_list


SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-hockeyke-development-only",
)
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    ["localhost", "127.0.0.1", "[::1]"],
)

CORS_ALLOWED_ORIGINS = env_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    ["http://localhost:5173", "http://localhost:5174"],
)
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

database_engine = os.environ.get("DJANGO_DB_ENGINE", "mysql").strip().lower()

if database_engine == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DJANGO_DB_NAME", "hkenewdb"),
            "USER": os.environ.get("DJANGO_DB_USER", "root"),
            "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD", ""),
            "HOST": os.environ.get("DJANGO_DB_HOST", "localhost"),
            "PORT": os.environ.get("DJANGO_DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }
elif database_engine == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.environ.get("DJANGO_DB_NAME", BASE_DIR / "db.sqlite3"),
        }
    }
else:
    raise ImproperlyConfigured(
        "DJANGO_DB_ENGINE must be either 'mysql' or 'sqlite' in development."
    )
