from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class AbstractToken(models.Model):
    """
    Abstract base model for one-time security tokens.

    Concrete implementations include:
        - EmailVerificationToken
        - PasswordResetToken
        - MagicLoginToken
        - InvitationToken
    """

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # -------------------------------------------------------------------------
    # Token
    # -------------------------------------------------------------------------

    token_hash = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        help_text="SHA-256 hash of the token.",
    )

    expires_at = models.DateTimeField()

    used_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    # -------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------

    @property
    def is_used(self) -> bool:
        return self.used_at is not None

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        return (
            not self.is_used
            and not self.is_expired
        )

    # -------------------------------------------------------------------------
    # Methods
    # -------------------------------------------------------------------------

    def mark_as_used(self) -> None:
        """
        Mark this token as consumed.
        """
        if self.used_at is None:
            self.used_at = timezone.now()
            self.save(update_fields=["used_at"])

    class Meta:
        abstract = True