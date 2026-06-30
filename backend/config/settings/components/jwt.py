from datetime import timedelta

from config.settings.env import env

JWT_ACCESS_MINUTES = env.int("JWT_ACCESS_MINUTES", default=15)
JWT_REFRESH_DAYS = env.int("JWT_REFRESH_DAYS", default=7)
JWT_ROTATE_REFRESH_TOKENS = env.bool("JWT_ROTATE_REFRESH_TOKENS", default=True)
JWT_BLACKLIST_AFTER_ROTATION = env.bool("JWT_BLACKLIST_AFTER_ROTATION", default=True)
JWT_UPDATE_LAST_LOGIN = env.bool("JWT_UPDATE_LAST_LOGIN", default=True)
JWT_ALGORITHM = env("JWT_ALGORITHM", default="HS256")
JWT_SIGNING_KEY = env("JWT_SIGNING_KEY", default=env("DJANGO_SECRET_KEY"))

SIMPLE_JWT = {
    # Token lifetime
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=JWT_ACCESS_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=JWT_REFRESH_DAYS),

    # Refresh behavior
    "ROTATE_REFRESH_TOKENS": JWT_ROTATE_REFRESH_TOKENS,
    "BLACKLIST_AFTER_ROTATION": JWT_BLACKLIST_AFTER_ROTATION,
    "UPDATE_LAST_LOGIN": JWT_UPDATE_LAST_LOGIN,

    # Cryptography
    "ALGORITHM": JWT_ALGORITHM,
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": env("JWT_AUDIENCE", default=None),
    "ISSUER": env("JWT_ISSUER", default=None),
    "LEEWAY": env.int("JWT_LEEWAY", default=0),

    # Header
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",

    # Claims
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",

    # Token classes
    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
    ),
    "TOKEN_OBTAIN_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenObtainPairSerializer"
    ),
    "TOKEN_REFRESH_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenRefreshSerializer"
    ),
    "TOKEN_VERIFY_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenVerifySerializer"
    ),
    "TOKEN_BLACKLIST_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenBlacklistSerializer"
    ),

    # Sliding tokens (disabled by default)
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}