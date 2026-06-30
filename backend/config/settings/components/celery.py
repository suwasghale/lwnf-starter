"""
===============================================================================
Celery Configuration
===============================================================================

This module contains all Celery-related settings.

Celery uses Redis as:

- Message Broker
- Result Backend

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

REDIS_CELERY_DB = env.int(
    "REDIS_CELERY_DB",
    default=0,
)


def build_redis_url(database: int) -> str:
    """
    Build Redis URL for Celery.
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


CELERY_REDIS_URL = build_redis_url(
    REDIS_CELERY_DB
)

# =============================================================================
# Broker
# =============================================================================

CELERY_BROKER_URL = CELERY_REDIS_URL

CELERY_RESULT_BACKEND = CELERY_REDIS_URL

# =============================================================================
# Serialization
# =============================================================================

CELERY_ACCEPT_CONTENT = [
    "json",
]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

# =============================================================================
# Time
# =============================================================================

CELERY_ENABLE_UTC = True

CELERY_TIMEZONE = "UTC"

# =============================================================================
# Task Behaviour
# =============================================================================

CELERY_TASK_TRACK_STARTED = True

CELERY_TASK_IGNORE_RESULT = False

CELERY_TASK_ACKS_LATE = True

CELERY_TASK_REJECT_ON_WORKER_LOST = True

CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# =============================================================================
# Limits
# =============================================================================

CELERY_TASK_SOFT_TIME_LIMIT = env.int(
    "CELERY_TASK_SOFT_TIME_LIMIT",
    default=1500,
)

CELERY_TASK_TIME_LIMIT = env.int(
    "CELERY_TASK_TIME_LIMIT",
    default=1800,
)

CELERY_RESULT_EXPIRES = env.int(
    "CELERY_RESULT_EXPIRES",
    default=3600,
)

# =============================================================================
# Workers
# =============================================================================

CELERY_WORKER_CONCURRENCY = env.int(
    "CELERY_WORKER_CONCURRENCY",
    default=4,
)

CELERY_WORKER_MAX_TASKS_PER_CHILD = env.int(
    "CELERY_MAX_TASKS_PER_CHILD",
    default=100,
)

CELERY_WORKER_MAX_MEMORY_PER_CHILD = env.int(
    "CELERY_MAX_MEMORY_PER_CHILD",
    default=256000,
)

# =============================================================================
# Beat
# =============================================================================

CELERY_BEAT_SCHEDULER = (
    "django_celery_beat.schedulers.DatabaseScheduler"
)