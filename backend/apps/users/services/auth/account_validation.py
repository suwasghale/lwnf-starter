"""
Account validation rules.
"""

from __future__ import annotations

from apps.users.models import User

from apps.users.exceptions.authentication import (
    InactiveAccount,
    EmailNotVerified,
)


def validate_account(
    *,
    user: User,
) -> None:
    """
    Validate that a user may authenticate.
    """

    if not user.is_active:
        raise InactiveAccount()

    if not user.is_verified:
        raise EmailNotVerified()