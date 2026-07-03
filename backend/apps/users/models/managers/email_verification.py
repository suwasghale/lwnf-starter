"""
Custom manager for EmailVerificationToken.
"""

from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.utils import timezone


class EmailVerificationTokenManager(
    models.Manager["EmailVerificationToken"]
):
    """
    Custom manager for email verification tokens.
    """

    def get_queryset(self):
        """
        Return the default queryset.
        """
        return super().get_queryset().select_related("user")

    def active(self):
        """
        Return active verification tokens.
        """
        now = timezone.now()

        return (
            self.get_queryset()
            .filter(
                used_at__isnull=True,
                expires_at__gt=now,
            )
        )

    def expired(self):
        """
        Return expired verification tokens.
        """
        return (
            self.get_queryset()
            .filter(
                expires_at__lte=timezone.now(),
            )
        )

    def used(self):
        """
        Return used verification tokens.
        """
        return (
            self.get_queryset()
            .filter(
                used_at__isnull=False,
            )
        )

    def unused(self):
        """
        Return unused verification tokens.
        """
        return (
            self.get_queryset()
            .filter(
                used_at__isnull=True,
            )
        )

    def create_token(
        self,
        *,
        user,
        token_hash: str,
        expires_in: timedelta = timedelta(hours=24),
        created_ip: str | None = None,
        user_agent: str = "",
    ):
        """
        Create a verification token.

        The token_hash must already be hashed.
        Token generation belongs to the service layer.
        """
        return self.create(
            user=user,
            token_hash=token_hash,
            expires_at=timezone.now() + expires_in,
            created_ip=created_ip,
            user_agent=user_agent,
        )