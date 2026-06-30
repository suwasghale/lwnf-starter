"""
Static and media configuration.
"""

from config.settings.env import BASE_DIR

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"