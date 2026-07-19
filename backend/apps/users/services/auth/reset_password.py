"""
Password reset service.

Responsibilities:
    - Verify a password reset token.
    - Change the user's password.
    - Consume every remaining password reset token.

This service does not:
    - Generate tokens.
    - Send emails.
"""

from __future__ import annotations

from django.db import transaction

from apps.users.models import User
from apps.users.models.tokens import PasswordResetToken

from apps.users.services.tokens.password_reset import (
    verify_password_reset_token,
)

from apps.users.services.user import (
    change_password,
)


@transaction.atomic
def reset_password(
    *,
    raw_token: str,
    new_password: str,
) -> User:
    """
    Reset a user's password.

    Workflow:
        1. Verify the reset token.
        2. Update the user's password.
        3. Consume every remaining password reset token.
        4. Return the updated user.

    Raises:
        PasswordResetTokenInvalid
    """

    token = verify_password_reset_token(
        raw_token=raw_token,
    )

    user = token.user

    change_password(
        user=user,
        password=new_password,
    )

    PasswordResetToken.objects.consume_unused_tokens(
        user=user,
    )

    return user