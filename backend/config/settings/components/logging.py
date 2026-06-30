"""
===============================================================================
Logging Configuration
===============================================================================

Centralized logging configuration for the entire project.

Logs are separated into:

- Django
- Celery
- Security
- Errors

Future:

- JSON Logs
- ELK
- Loki
- Grafana
===============================================================================
"""

from pathlib import Path

from logging.handlers import RotatingFileHandler

from config.settings.env import BASE_DIR
from config.settings.env import env

# =============================================================================
# Log Directory
# =============================================================================

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    exist_ok=True,
)

# =============================================================================
# Environment
# =============================================================================

LOG_LEVEL = env(
    "LOG_LEVEL",
    default="INFO",
).upper()

LOG_MAX_BYTES = env.int(
    "LOG_MAX_BYTES",
    default=10 * 1024 * 1024,
)

LOG_BACKUP_COUNT = env.int(
    "LOG_BACKUP_COUNT",
    default=10,
)

# =============================================================================
# Formatter
# =============================================================================

STANDARD_FORMAT = (
    "[{asctime}] "
    "{levelname:<8} "
    "{name:<30} "
    "{message}"
)

VERBOSE_FORMAT = (
    "[{asctime}] "
    "{levelname:<8} "
    "{name:<35} "
    "{module:<20} "
    "{funcName:<25} "
    "{lineno:<5} "
    "{message}"
)

SIMPLE_FORMAT = (
    "{levelname}: {message}"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# =============================================================================
# Formatters
# =============================================================================

FORMATTERS = {
    "standard": {
        "format": STANDARD_FORMAT,
        "style": "{",
        "datefmt": DATE_FORMAT,
    },
    "verbose": {
        "format": VERBOSE_FORMAT,
        "style": "{",
        "datefmt": DATE_FORMAT,
    },
    "simple": {
        "format": SIMPLE_FORMAT,
        "style": "{",
    },
}

# =============================================================================
# Filters
# =============================================================================

FILTERS = {}

# =============================================================================
# Log Files
# =============================================================================

DJANGO_LOG_FILE = LOG_DIR / "django.log"

ERROR_LOG_FILE = LOG_DIR / "errors.log"

CELERY_LOG_FILE = LOG_DIR / "celery.log"

SECURITY_LOG_FILE = LOG_DIR / "security.log"

# =============================================================================
# Handlers
# =============================================================================

HANDLERS = {
    # -------------------------------------------------------------------------
    # Console
    # -------------------------------------------------------------------------
    "console": {
        "class": "logging.StreamHandler",
        "formatter": "standard",
        "level": LOG_LEVEL,
    },
    # -------------------------------------------------------------------------
    # Django
    # -------------------------------------------------------------------------
    "django_file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": DJANGO_LOG_FILE,
        "formatter": "verbose",
        "level": LOG_LEVEL,
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
    },
    # -------------------------------------------------------------------------
    # Errors
    # -------------------------------------------------------------------------
    "error_file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": ERROR_LOG_FILE,
        "formatter": "verbose",
        "level": "ERROR",
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
    },
    # -------------------------------------------------------------------------
    # Celery
    # -------------------------------------------------------------------------
    "celery_file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": CELERY_LOG_FILE,
        "formatter": "verbose",
        "level": LOG_LEVEL,
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
    },
    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    "security_file": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": SECURITY_LOG_FILE,
        "formatter": "verbose",
        "level": "WARNING",
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
        "delay": True,
    },
}