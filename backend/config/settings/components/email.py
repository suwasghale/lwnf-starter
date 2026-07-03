"""
===============================================================================
LWNF Backend - Email Configuration
===============================================================================

Centralized email settings for development and production.

Features
--------
- Environment-driven configuration
- SMTP backend
- Console backend for development
- TLS / SSL support
- HTML email ready
- Celery compatible
- Future provider support (SES, SendGrid, Mailgun, Brevo)

===============================================================================
"""

from config.settings.env import env

# =============================================================================
# Backend Selection
# =============================================================================

EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if env.bool("DEBUG", default=True)
    else env(
        "EMAIL_BACKEND",
        default="django.core.mail.backends.smtp.EmailBackend",
    )
)

# =============================================================================
# SMTP Configuration
# =============================================================================

EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)

EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")

EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)

EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=30)

# =============================================================================
# Default Addresses
# =============================================================================

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="no-reply@lwnf.org",
)

EMAIL_SITE_NAME = env(
    "EMAIL_SITE_NAME",
    default="L.W.N.F",
)

SERVER_EMAIL = env(
    "SERVER_EMAIL",
    default=DEFAULT_FROM_EMAIL,
)

EMAIL_SUBJECT_PREFIX = env(
    "EMAIL_SUBJECT_PREFIX",
    default="[LWNF] ",
)

# =============================================================================
# Admin Notifications
# =============================================================================

ADMINS = [
    (
        env("ADMIN_NAME", default="Administrator"),
        env("ADMIN_EMAIL", default="admin@lwnf.org"),
    ),
]

MANAGERS = ADMINS

# =============================================================================
# Email Behaviour
# =============================================================================

EMAIL_USE_LOCALTIME = True

EMAIL_SSL_CERTFILE = env(
    "EMAIL_SSL_CERTFILE",
    default=None,
)

EMAIL_SSL_KEYFILE = env(
    "EMAIL_SSL_KEYFILE",
    default=None,
)

# =============================================================================
# Future Provider Settings
# =============================================================================

EMAIL_PROVIDER = env(
    "EMAIL_PROVIDER",
    default="smtp",
)

# smtp
# sendgrid
# ses
# mailgun
# brevo

# =============================================================================
# Email Templates
# =============================================================================

EMAIL_TEMPLATE_DIR = "emails"

# =============================================================================
# Attachment Limits
# =============================================================================

EMAIL_MAX_ATTACHMENT_SIZE = env.int(
    "EMAIL_MAX_ATTACHMENT_SIZE",
    default=10 * 1024 * 1024,
)

# =============================================================================
# Retry Configuration (used by Celery tasks)
# =============================================================================

EMAIL_MAX_RETRIES = env.int(
    "EMAIL_MAX_RETRIES",
    default=3,
)

EMAIL_RETRY_DELAY = env.int(
    "EMAIL_RETRY_DELAY",
    default=60,
)

