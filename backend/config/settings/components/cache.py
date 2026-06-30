"""
===============================================================================
Django Cache Configuration
===============================================================================

This module configures Django's caching framework using Redis.

Why Redis?
----------
- High performance
- Shared cache across multiple Django instances
- Production-ready
- Works seamlessly with Celery

References:
- https://docs.djangoproject.com/en/stable/topics/cache/
- https://github.com/jazzband/django-redis
===============================================================================
"""

from config.settings.env import env


# =============================================================================
# Redis Connection
# =============================================================================

REDIS_HOST = env(
    "REDIS_HOST",
    default="redis",
)

REDIS_PORT = env.int(
    "REDIS_PORT",
    default=6379,
)

REDIS_PASSWORD = env(
    "REDIS_PASSWORD",
    default="",
)

REDIS_CACHE_DB = env.int(
    "REDIS_CACHE_DB",
    default=1,
)


def build_redis_url(database: int) -> str:
    """
    Build a Redis connection URL.

    Example:
        redis://localhost:6379/1

        redis://:password@localhost:6379/1
    """

    if REDIS_PASSWORD:
        return (
            f"redis://:{REDIS_PASSWORD}@"
            f"{REDIS_HOST}:{REDIS_PORT}/{database}"
        )

    return (
        f"redis://"
        f"{REDIS_HOST}:{REDIS_PORT}/{database}"
    )


CACHE_REDIS_URL = build_redis_url(
    REDIS_CACHE_DB
)

# =============================================================================
# Django Cache
# =============================================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHE_REDIS_URL,
        "TIMEOUT": env.int(
            "CACHE_TIMEOUT",
            default=300,
        ),
        "KEY_PREFIX": env(
            "CACHE_KEY_PREFIX",
            default="lwnf",
        ),
        "VERSION": 1,
        "OPTIONS": {
            "CLIENT_CLASS": (
                "django_redis.client.DefaultClient"
            ),
            "IGNORE_EXCEPTIONS": True,
        },
    },
}