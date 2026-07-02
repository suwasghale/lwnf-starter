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

PROFILE_IMAGE_UPLOAD_TO = "users/profile-images/"

PROFILE_IMAGE_MAX_SIZE = 5 * 1024 * 1024  # 5 MB

PROFILE_IMAGE_ALLOWED_EXTENSIONS = (
    "jpg",
    "jpeg",
    "png",
    "webp",
)

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
# File Names
# =============================================================================

DEFAULT_PROFILE_IMAGE = "defaults/profile.png"

# =============================================================================
# Regex Patterns
# =============================================================================

PHONE_NUMBER_REGEX = r"^\+?[0-9]{7,20}$"

USERNAME_REGEX = r"^[a-zA-Z0-9._-]+$"