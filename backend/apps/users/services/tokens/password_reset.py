"""
Password reset token services.
"""

from __future__ import annotations

from apps.users.models import (
    User,
)
from apps.users.models.tokens.password_reset import (
    PasswordResetToken,
)

def create_password_reset_token(
    *,
    user: User,
) -> PasswordResetToken:
    """
    Create a new password reset token.
    """

    return PasswordResetToken.objects.create(
        user=user,
    )