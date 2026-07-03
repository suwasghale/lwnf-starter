"""
Email verification token model.

This model stores hashed verification tokens used to verify a user's
email address after registration.

Security:
- Never store raw tokens.
- Store only a SHA-256 hash.
- Raw tokens are generated and emailed by the service layer.

Business logic such as generating tokens, hashing, sending emails,
and validation belongs in the service layer.
"""

from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone

from apps.users.models import User
from apps.users.models.managers import EmailVerificationTokenManager


class EmailVerificationToken(models.Model):
    """
    Email verification token.
    """

    id: models.UUIDField = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Unique identifier for this verification token.",
    )

    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
        verbose_name="User",
        help_text="User associated with this verification token.",
    )

    token_hash: models.CharField = models.CharField(
        max_length=64,
        unique=True,
        db_index=True,
        verbose_name="Token hash",
        help_text="SHA-256 hash of the verification token.",
    )

    expires_at: models.DateTimeField = models.DateTimeField(
        verbose_name="Expires at",
        help_text="Date and time when this token expires.",
    )

    used_at: models.DateTimeField = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Used at",
        help_text="Date and time when this token was used.",
    )

    created_ip: models.GenericIPAddressField = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Created IP",
        help_text="IP address used to request this verification token.",
    )

    user_agent: models.TextField = models.TextField(
        blank=True,
        verbose_name="User agent",
        help_text="Browser/device used to request this verification token.",
    )

    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )

    objects = EmailVerificationTokenManager()

    class Meta:
        verbose_name = "Email verification token"
        verbose_name_plural = "Email verification tokens"

        ordering = ("-created_at",)

        indexes = [
            models.Index(fields=["user"], name="evt_user_idx"),
            models.Index(fields=["expires_at"], name="evt_expiry_idx"),
            models.Index(fields=["used_at"], name="evt_used_idx"),
            models.Index(fields=["created_at"], name="evt_created_idx"),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["token_hash"],
                name="unique_email_verification_token_hash",
            )
        ]

    @property
    def is_used(self) -> bool:
        """
        Whether this token has already been used.
        """
        return self.used_at is not None

    @property
    def is_expired(self) -> bool:
        """
        Whether this token has expired.
        """
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self) -> bool:
        """
        Whether this token is currently valid.
        """
        return (
            not self.is_used
            and not self.is_expired
        )

    def mark_as_used(self) -> None:
        """
        Mark this token as used.
        """
        if self.used_at is None:
            self.used_at = timezone.now()
            self.save(update_fields=["used_at"])

    def __str__(self) -> str:
        return f"Email verification token for {self.user.email}"