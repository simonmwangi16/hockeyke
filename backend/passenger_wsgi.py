"""Passenger entry point for the HockeyKE Django application."""

import os
import sys
from pathlib import Path


APPLICATION_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(APPLICATION_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application  # noqa: E402,F401
