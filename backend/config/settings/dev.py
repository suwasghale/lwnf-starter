"""
core/settings/dev.py — Local development only.

Usage:
    DJANGO_SETTINGS_MODULE=core.settings.dev python manage.py runserver

Never used in staging or production.
"""
from .base import *  # noqa: F401, F403

DEBUG         = env.bool("DEBUG")
ALLOWED_HOSTS = ["*"]
