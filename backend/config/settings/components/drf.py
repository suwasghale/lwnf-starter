from config.settings.env import env

API_PAGE_SIZE = env.int("API_PAGE_SIZE", default=20)
MAX_API_PAGE_SIZE = env.int("MAX_API_PAGE_SIZE", default=100)
ENABLE_BROWSABLE_API = env.bool("ENABLE_BROWSABLE_API", default=True)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ] if ENABLE_BROWSABLE_API else [
            "rest_framework.renderers.JSONRenderer",
        ]
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": API_PAGE_SIZE,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": env("DRF_THROTTLE_ANON", default="100/hour"),
        "user": env("DRF_THROTTLE_USER", default="1000/hour"),
    },
    "EXCEPTION_HANDLER": "core.exceptions.handlers.custom_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "SEARCH_PARAM": "search",
    "ORDERING_PARAM": "ordering",
    "COERCE_DECIMAL_TO_STRING": True,
    "UNICODE_JSON": True,
    "COMPACT_JSON": False,
}