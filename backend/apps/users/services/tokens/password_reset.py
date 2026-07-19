"""
Password reset token services.
"""

from __future__ import annotations


from dataclasses import dataclass
from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from config.settings.env import env

from apps.users.models import (
    User,
)

from apps.users.models.tokens.password_reset import (
    PasswordResetToken,     
)

from core.security.tokens import (
    generate_hashed_token,
)


# =============================================================================
# Settings
# =============================================================================

PASSWORD_RESET_TOKEN_BYTES = env.int(
    "PASSWORD_RESET_TOKEN_BYTES",
    default=32,
)

PASSWORD_RESET_TOKEN_EXPIRY_MINUTES = env.int(
    "PASSWORD_RESET_TOKEN_EXPIRY_MINUTES",
    default=30,
)


# =============================================================================
# DTO
# =============================================================================


@dataclass(slots=True)
class PasswordResetTokenResult:
    """
    Newly created password reset token.

    The raw token should ONLY be used for emailing
    the user and must never be stored.
    """

    token: PasswordResetToken
    raw_token: str


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def create_password_reset_token(
    *,
    user: User,
    created_ip: str | None = None,
    user_agent: str = "",
) -> PasswordResetTokenResult:
    """
    Create a new password reset token.

    The database stores only the SHA-256 hash.
    The raw token is returned so it can be sent
    to the user via email.

    Args:
        user:
            User requesting a password reset.

        created_ip:
            IP address from which the request originated.

        user_agent:
            Browser/device information.

    Returns:
        PasswordResetTokenResult
    """

    raw_token, token_hash = generate_hashed_token(
        nbytes=PASSWORD_RESET_TOKEN_BYTES,
    )

    expires_at = timezone.now() + timedelta(
        minutes=PASSWORD_RESET_TOKEN_EXPIRY_MINUTES,
    )

    token = PasswordResetToken.objects.create_password_reset_token(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
        created_ip=created_ip,
        user_agent=user_agent,
    )

    return PasswordResetTokenResult(
        token=token,
        raw_token=raw_token,
    )
    
@transaction.atomic
def invalidate_password_reset_tokens(
        *,
        user: User,
    ) -> int:
        """
        Invalidate every unused password reset token
        belonging to a user.

        Returns:
            Number of invalidated tokens.
        """

        return PasswordResetToken.objects.invalidate_unused_tokens(
            user=user,
        )