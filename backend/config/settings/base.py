"""Settings shared by every HockeyKE environment."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False

    raise ImproperlyConfigured(
        f"{name} must be one of: 1, 0, true, false, yes, no, on, off."
    )


def env_list(name, default=()):
    value = os.environ.get(name)
    if value is None:
        return list(default)
    return [item.strip() for item in value.split(",") if item.strip()]


def required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(
            f"{name} is required when HOCKEYKE_ENV=production."
        )
    if value.lower().startswith(("required-", "change-me", "placeholder")):
        raise ImproperlyConfigured(
            f"{name} must not use a placeholder value when "
            "HOCKEYKE_ENV=production."
        )
    return value


# Application definition

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'corsheaders',

    # Local apps
    'core',
    'competitions',
    'teams',
    'matches',
    'players',
    'stats',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path(
    os.environ.get("DJANGO_MEDIA_ROOT", BASE_DIR / "media")
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Jazzmin settings
JAZZMIN_SETTINGS = {
    "site_title": "HockeyKE Admin",
    "site_header": "HockeyKE",
    "site_brand": "HockeyKE",

    "welcome_sign": "Welcome to HockeyKE Admin",
    "copyright": "HockeyKE",

    "show_sidebar": True,
    "navigation_expanded": True,

    "order_with_respect_to": [
        "competitions",
        "competitions.Season",
        "competitions.League",
        "competitions.LeagueSeason",

        "teams",
        "teams.MenTeam",
        "teams.WomenTeam",
        "teams.TeamLeagueSeason",

        "players",

        "matches",
        "matches.Match",
        "matches.PremierLeagueMenMatch",
        "matches.SuperLeagueMenMatch",
        "matches.NationalLeagueCentralZoneMatch",
        "matches.NationalLeagueEasternZoneMatch",
        "matches.NationalLeagueSouthernZoneMatch",
        "matches.NationalLeagueWesternZoneMatch",
        "matches.PremierLeagueWomenMatch",
        "matches.SuperLeagueWomenMatch",
        "matches.MatchEvent",

        "stats",
        "stats.Standings",
        "auth",
    ],

    "icons": {
        "competitions": "fas fa-trophy",
        "competitions.Season": "fas fa-calendar-alt",
        "competitions.League": "fas fa-medal",
        "competitions.LeagueSeason": "fas fa-layer-group",

        "teams": "fas fa-users",
        "teams.MenTeam": "fas fa-male",
        "teams.WomenTeam": "fas fa-female",
        "teams.TeamLeagueSeason": "fas fa-random",

        "players": "fas fa-user",
        "matches": "fas fa-calendar-check",
        "matches.Match": "fas fa-hockey-puck",
        "stats": "fas fa-chart-bar",

        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user-shield",
        "auth.Group": "fas fa-users-cog",
    },
}
