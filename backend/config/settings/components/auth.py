from datetime import timedelta

from config.settings.env import env

EMAIL_VERIFICATION_TOKEN_LIFETIME = timedelta(
    hours=env.int(
        "EMAIL_VERIFICATION_TOKEN_LIFETIME_HOURS",
        default=24,
    )
)

PASSWORD_RESET_TOKEN_LIFETIME = timedelta(
    minutes=env.int(
        "PASSWORD_RESET_TOKEN_LIFETIME_MINUTES",
        default=30,
    )
)

FRONTEND_URL = env(
    "FRONTEND_URL",
    default="http://localhost:3000",
)

FRONTEND_VERIFY_EMAIL_URL = (
    f"{FRONTEND_URL}/verify-email"
)

FRONTEND_PASSWORD_RESET_URL = (
    f"{FRONTEND_URL}/reset-password"
)