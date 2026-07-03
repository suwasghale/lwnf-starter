"""
Custom manager for EmailVerificationToken.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from apps.users.models import User
    from apps.users.models.tokens.email_verification import (
        EmailVerificationToken,
    )


class EmailVerificationTokenManager(
    models.Manager["EmailVerificationToken"]
):
    """
    Custom manager for EmailVerificationToken.
    """

    def get_queryset(
        self,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return the default queryset with related user loaded.
        """
        return (
            super()
            .get_queryset()
            .select_related("user")
        )

    def valid(
        self,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return valid (unused and unexpired) tokens.
        """
        now = timezone.now()

        return (
            self.get_queryset()
            .filter(
                used_at__isnull=True,
                expires_at__gt=now,
            )
        )

    def expired(
        self,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return expired tokens.
        """
        return (
            self.get_queryset()
            .filter(
                expires_at__lte=timezone.now(),
            )
        )

    def used(
        self,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return used tokens.
        """
        return (
            self.get_queryset()
            .filter(
                used_at__isnull=False,
            )
        )

    def unused(
        self,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return unused tokens.
        """
        return (
            self.get_queryset()
            .filter(
                used_at__isnull=True,
            )
        )

    def for_user(
        self,
        user: User,
    ) -> models.QuerySet["EmailVerificationToken"]:
        """
        Return all verification tokens belonging to a user.
        """
        return (
            self.get_queryset()
            .filter(user=user)
        )

    def latest_for_user(
        self,
        user: User,
    ) -> EmailVerificationToken | None:
        """
        Return the latest verification token for a user.
        """
        return (
            self.for_user(user)
            .order_by("-created_at")
            .first()
        )

    def invalidate_user_tokens(
        self,
        user: User,
    ) -> int:
        """
        Mark every valid token for the given user as used.

        Returns:
            Number of invalidated tokens.
        """
        return (
            self.valid()
            .filter(user=user)
            .update(
                used_at=timezone.now(),
            )
        )

    def create_token(
        self,
        *,
        user: User,
        token_hash: str,
        expires_at,
        created_ip: str | None = None,
        user_agent: str = "",
    ) -> EmailVerificationToken:
        """
        Persist a new email verification token.

        Notes:
            - The token must already be hashed.
            - Expiration must already be calculated.
            - Token generation belongs to the service layer.
        """
        return self.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
            created_ip=created_ip,
            user_agent=user_agent,
        )