"""Select HockeyKE settings from the explicit runtime environment."""

import os

from django.core.exceptions import ImproperlyConfigured


ENVIRONMENT = os.environ.get("HOCKEYKE_ENV", "development").strip().lower()

if ENVIRONMENT == "development":
    from .development import *  # noqa: F403
elif ENVIRONMENT == "production":
    from .production import *  # noqa: F403
else:
    raise ImproperlyConfigured(
        "HOCKEYKE_ENV must be either 'development' or 'production'."
    )
