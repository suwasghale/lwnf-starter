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