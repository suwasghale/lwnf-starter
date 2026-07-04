"""
Custom manager for PasswordResetToken.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from django.db import models

from ..querysets import PasswordResetTokenQuerySet

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.users.models.tokens.password_reset import (
        PasswordResetToken,
    )


class PasswordResetTokenManager(
    models.Manager.from_queryset(
        PasswordResetTokenQuerySet,
    )
):
    """
    Custom manager for PasswordResetToken.
    """

    def create_password_reset_token(
        self,
        *,
        user: User,
        token_hash: str,
        expires_at: datetime,
        created_ip: str | None = None,
        user_agent: str = "",
    ) -> PasswordResetToken:
        """
        Persist a new password reset token.

        Notes:
            - The token must already be hashed.
            - The expiration datetime must already be calculated.
            - Token generation belongs to the service layer.
        """
        return self.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
            created_ip=created_ip,
            user_agent=user_agent,
        )