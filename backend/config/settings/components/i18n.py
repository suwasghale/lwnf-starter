"""
Internationalization configuration.
"""

from config.settings.env import BASE_DIR

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ("en", "English"),
    ("fr", "Français"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]