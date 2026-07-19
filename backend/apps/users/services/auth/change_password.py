"""
Business logic for changing the authenticated user's password.
"""

from __future__ import annotations

from django.conf import settings

from apps.users.models import User

from apps.users.services.auth.password_validation import (
    validate_current_password,
    validate_new_password,
)

# Optional
# from apps.users.services.auth.sessions import (
#     revoke_all_refresh_tokens,
# )


# =============================================================================
# Public API
# =============================================================================


def change_password(
    *,
    user: User,
    current_password: str,
    new_password: str,
) -> None:
    """
    Change the authenticated user's password.

    Steps:

    1. Verify current password
    2. Validate new password
    3. Hash and save password
    4. Optionally revoke all refresh tokens
    """

    validate_current_password(
        user=user,
        current_password=current_password,
    )

    validate_new_password(
        user=user,
        new_password=new_password,
    )

    user.set_password(
        new_password,
    )

    user.save(
        update_fields=[
            "password",
        ],
    )

    # Optional (recommended in production)
    #
    # if settings.PASSWORD_CHANGE_REVOKE_ALL_SESSIONS:
    #     revoke_all_refresh_tokens(user=user)