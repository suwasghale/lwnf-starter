"""
LWNF Backend - Session Configuration
"""

from config.settings.env import env

SESSION_ENGINE = env(
    "SESSION_ENGINE",
    default="django.contrib.sessions.backends.cached_db",
)

SESSION_COOKIE_NAME = env("SESSION_COOKIE_NAME", default="lwnf_sessionid")
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", default=60 * 60 * 24 * 14)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
SESSION_COOKIE_SAMESITE = env("SESSION_COOKIE_SAMESITE", default="Lax")
SESSION_SAVE_EVERY_REQUEST = env.bool("SESSION_SAVE_EVERY_REQUEST", default=False)
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE",
    default=False,
)

SESSION_CACHE_ALIAS = "default"

CSRF_USE_SESSIONS = False

CSRF_COOKIE_NAME = env("CSRF_COOKIE_NAME", default="csrftoken")
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
CSRF_COOKIE_SAMESITE = env("CSRF_COOKIE_SAMESITE", default="Lax")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"
