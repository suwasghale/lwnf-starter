"""
===============================================================================
LWNF Backend - User Constants
===============================================================================

Centralized constants for the Users application.

===============================================================================
"""

# =============================================================================
# User Model
# =============================================================================

USERNAME_MAX_LENGTH = 50

EMAIL_MAX_LENGTH = 254

FIRST_NAME_MAX_LENGTH = 100

LAST_NAME_MAX_LENGTH = 100

PHONE_NUMBER_MAX_LENGTH = 20

# =============================================================================
# Profile
# =============================================================================

BIO_MAX_LENGTH = 1000

# =============================================================================
# Avatar
# =============================================================================

AVATAR_UPLOAD_PATH = "media/avatars"

AVATAR_MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

AVATAR_ALLOWED_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "webp",
)

AVATAR_ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

DEFAULT_AVATAR = "defaults/avatar.webp"

AVATAR_OUTPUT_SIZE = (512, 512)

AVATAR_OUTPUT_FORMAT = "WEBP"

AVATAR_OUTPUT_QUALITY = 85

# =============================================================================
# Address
# =============================================================================

ADDRESS_LINE_MAX_LENGTH = 255

CITY_MAX_LENGTH = 100

STATE_MAX_LENGTH = 100

POSTAL_CODE_MAX_LENGTH = 20

COUNTRY_MAX_LENGTH = 100

# =============================================================================
# Authentication
# =============================================================================

PASSWORD_MIN_LENGTH = 8

OTP_LENGTH = 6

OTP_EXPIRATION_MINUTES = 10

PASSWORD_RESET_TOKEN_EXPIRATION_HOURS = 24

EMAIL_VERIFICATION_EXPIRATION_HOURS = 24

MAX_LOGIN_ATTEMPTS = 5

ACCOUNT_LOCKOUT_MINUTES = 30

# =============================================================================
# Pagination
# =============================================================================

DEFAULT_PAGE_SIZE = 20

MAX_PAGE_SIZE = 100

# =============================================================================
# Cache Keys
# =============================================================================

USER_CACHE_PREFIX = "user"

PROFILE_CACHE_PREFIX = "profile"

USER_PERMISSIONS_CACHE_PREFIX = "user_permissions"


# =============================================================================
# Regex Patterns
# =============================================================================

PHONE_NUMBER_REGEX = r"^\+?[0-9]{7,20}$"

USERNAME_REGEX = r"^[a-zA-Z0-9._-]+$"