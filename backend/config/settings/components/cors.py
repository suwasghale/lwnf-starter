"""
LWNF Backend - CORS Configuration
"""

from config.settings.env import DEBUG, env

CORS_ALLOW_ALL_ORIGINS = env.bool(
    "CORS_ALLOW_ALL_ORIGINS",
    default=DEBUG,
)

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[],
)

CORS_ALLOWED_ORIGIN_REGEXES = env.list(
    "CORS_ALLOWED_ORIGIN_REGEXES",
    default=[],
)

CORS_ALLOW_CREDENTIALS = env.bool(
    "CORS_ALLOW_CREDENTIALS",
    default=True,
)

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_EXPOSE_HEADERS = [
    "Content-Disposition",
]

CORS_PREFLIGHT_MAX_AGE = env.int(
    "CORS_PREFLIGHT_MAX_AGE",
    default=86400,
)