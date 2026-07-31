"""Production settings that reject incomplete security or database config."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import env_bool, env_list, required_env


SECRET_KEY = required_env("DJANGO_SECRET_KEY")
if len(SECRET_KEY) < 50 or SECRET_KEY.startswith("django-insecure-"):
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be a non-placeholder value of at least 50 characters "
        "when HOCKEYKE_ENV=production."
    )

DEBUG = False
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
if (
    not ALLOWED_HOSTS
    or "*" in ALLOWED_HOSTS
    or any(
        host.lower().startswith(("required-", "change-me", "placeholder"))
        for host in ALLOWED_HOSTS
    )
):
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS must contain explicit host names when "
        "HOCKEYKE_ENV=production."
    )

CORS_ALLOWED_ORIGINS = env_list("DJANGO_CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": required_env("DJANGO_DB_NAME"),
        "USER": required_env("DJANGO_DB_USER"),
        "PASSWORD": required_env("DJANGO_DB_PASSWORD"),
        "HOST": required_env("DJANGO_DB_HOST"),
        "PORT": os.environ.get("DJANGO_DB_PORT", "3306"),
        "CONN_MAX_AGE": int(os.environ.get("DJANGO_DB_CONN_MAX_AGE", "60")),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

STATIC_ROOT = Path(
    os.environ.get("DJANGO_STATIC_ROOT", BASE_DIR / "staticfiles")
)

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "3600"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    True,
)
SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
