"""
Django REST Framework configuration.
"""

from config.settings.env import env

# =============================================================================
# Pagination
# =============================================================================

API_PAGE_SIZE = env.int(
    "API_PAGE_SIZE",
    default=20,
)

MAX_API_PAGE_SIZE = env.int(
    "MAX_API_PAGE_SIZE",
    default=100,
)

# =============================================================================
# Renderer
# =============================================================================

ENABLE_BROWSABLE_API = env.bool(
    "ENABLE_BROWSABLE_API",
    default=True,
)

# =============================================================================
# Throttling
# =============================================================================

DEFAULT_THROTTLE_CLASSES: tuple[str, ...] = ()

DEFAULT_THROTTLE_RATES = {
    "public": env(
        "DRF_THROTTLE_PUBLIC",
        default="300/hour",
    ),
    "login": env(
        "DRF_THROTTLE_LOGIN",
        default="5/minute",
    ),
    "password_reset": env(
        "DRF_THROTTLE_PASSWORD_RESET",
        default="60/hour",
    ),
    "email_verification": env(
        "DRF_THROTTLE_EMAIL_VERIFICATION",
        default="5/hour",
    ),
    "registration": env(
        "DRF_THROTTLE_REGISTRATION",
        default="5/hour",
    ),
    "authenticated": env(
        "DRF_THROTTLE_AUTHENTICATED",
        default="1000/day",
    ),
    "password_change": env(
        "DRF_THROTTLE_PASSWORD_CHANGE",
        default="10/hour",
    ),
    "email_change": env(
        "DRF_THROTTLE_EMAIL_CHANGE",
        default="5/hour",
    ),
}

# =============================================================================
# REST Framework
# =============================================================================

REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    # Permissions
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    # Renderers
    "DEFAULT_RENDERER_CLASSES": (
        [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ]
        if ENABLE_BROWSABLE_API
        else [
            "rest_framework.renderers.JSONRenderer",
        ]
    ),

    # Parsers
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),

    # Pagination
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": API_PAGE_SIZE,
    "MAX_PAGE_SIZE": MAX_API_PAGE_SIZE,

    # Filtering
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),

    # OpenAPI
    "DEFAULT_SCHEMA_CLASS": (
        "drf_spectacular.openapi.AutoSchema"
    ),

    # Versioning
    "DEFAULT_VERSIONING_CLASS": (
        "rest_framework.versioning.NamespaceVersioning"
    ),

    # Throttling
    "DEFAULT_THROTTLE_CLASSES": DEFAULT_THROTTLE_CLASSES,
    "DEFAULT_THROTTLE_RATES": DEFAULT_THROTTLE_RATES,

    # Exception handler
    # (We'll implement this next.)
    "EXCEPTION_HANDLER": (
        "core.api.exceptions.custom_exception_handler"
    ),

    # Testing
    "TEST_REQUEST_DEFAULT_FORMAT": "json",

    # Search & Ordering
    "SEARCH_PARAM": "search",
    "ORDERING_PARAM": "ordering",

    # JSON
    "COERCE_DECIMAL_TO_STRING": True,
    "UNICODE_JSON": True,
    "COMPACT_JSON": False,
}