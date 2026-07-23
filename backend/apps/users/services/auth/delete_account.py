"""
Account deletion service.
"""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.users.exceptions.account import InvalidPassword
from apps.users.models import User
from apps.users.models.tokens import (
    EmailVerificationToken,
    EmailChangeToken,
    PasswordResetToken,
)


@transaction.atomic
def delete_account(
    *,
    user: User,
    password: str,
) -> None:
    """
    Delete the authenticated user's account.

    Workflow:

        - Verify current password.
        - Revoke all refresh tokens.
        - Invalidate all auth-related tokens.
        - Soft delete the account.
    """

    # -------------------------------------------------------------------------
    # Verify password
    # -------------------------------------------------------------------------

    if not user.check_password(password):
        raise InvalidPassword()

    # -------------------------------------------------------------------------
    # Revoke JWT refresh tokens
    # -------------------------------------------------------------------------

    OutstandingToken.objects.filter(
        user=user,
    ).delete()

    # -------------------------------------------------------------------------
    # Invalidate auth tokens
    # -------------------------------------------------------------------------

    EmailVerificationToken.objects.filter(
        user=user,
        used_at__isnull=True,
    ).update(
        used_at=timezone.now(),
    )

    EmailChangeToken.objects.filter(
        user=user,
        used_at__isnull=True,
    ).update(
        used_at=timezone.now(),
    )

    PasswordResetToken.objects.filter(
        user=user,
        used_at__isnull=True,
    ).update(
        used_at=timezone.now(),
    )

    # -------------------------------------------------------------------------
    # Soft delete account
    # -------------------------------------------------------------------------

    user.is_active = False

    user.deleted_at = timezone.now()
    
    user.set_unusable_password()

    user.save(
        update_fields=[
            "password",
            "is_active",
            "deleted_at",
        ],
    )