"""
===============================================================================
LWNF Backend - Storage Configuration
===============================================================================

Centralized object storage configuration.

Supports:
- Local filesystem (development)
- Cloudflare R2 (production)
- S3-compatible storage via django-storages

===============================================================================
"""

from config.settings.env import DEBUG, env

# =============================================================================
# Storage Backend Selection
# =============================================================================

USE_CLOUD_STORAGE = env.bool("USE_CLOUD_STORAGE", default=not DEBUG)

if USE_CLOUD_STORAGE:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# =============================================================================
# Cloudflare R2 Credentials
# =============================================================================

AWS_ACCESS_KEY_ID = env("R2_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("R2_SECRET_ACCESS_KEY", default="")

AWS_STORAGE_BUCKET_NAME = env("R2_BUCKET_NAME", default="")

AWS_S3_ENDPOINT_URL = env("R2_ENDPOINT_URL", default="")

AWS_S3_REGION_NAME = env("R2_REGION", default="auto")

AWS_S3_CUSTOM_DOMAIN = env("R2_CUSTOM_DOMAIN", default="")

# =============================================================================
# Object Parameters
# =============================================================================

AWS_DEFAULT_ACL = None

AWS_QUERYSTRING_AUTH = env.bool(
    "R2_QUERYSTRING_AUTH",
    default=False,
)

AWS_QUERYSTRING_EXPIRE = env.int(
    "R2_QUERYSTRING_EXPIRE",
    default=3600,
)

AWS_S3_FILE_OVERWRITE = False

AWS_S3_ADDRESSING_STYLE = "virtual"

AWS_IS_GZIPPED = True

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": env(
        "R2_CACHE_CONTROL",
        default="max-age=86400",
    ),
}

# =============================================================================
# File Locations
# =============================================================================

MEDIA_URL = (
    f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    if USE_CLOUD_STORAGE and AWS_S3_CUSTOM_DOMAIN
    else "/media/"
)

MEDIA_ROOT = "media"

STATIC_URL = "/static/"
STATIC_ROOT = "staticfiles"

# =============================================================================
# Upload Limits
# =============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = env.int(
    "FILE_UPLOAD_MAX_MEMORY_SIZE",
    default=10 * 1024 * 1024,
)

DATA_UPLOAD_MAX_MEMORY_SIZE = env.int(
    "DATA_UPLOAD_MAX_MEMORY_SIZE",
    default=20 * 1024 * 1024,
)
DATA_UPLOAD_MAX_NUMBER_FIELDS = env.int(
    "DATA_UPLOAD_MAX_NUMBER_FIELDS",
    default=1000,
)

DATA_UPLOAD_MAX_NUMBER_FILES = env.int(
    "DATA_UPLOAD_MAX_NUMBER_FILES",
    default=100,
)

FILE_UPLOAD_PERMISSIONS = 0o644

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

