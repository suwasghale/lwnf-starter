"""
Logout from every device.

Blacklists every outstanding refresh token belonging to the user.
"""

from __future__ import annotations

from django.db import transaction

from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from apps.users.models import User


@transaction.atomic
def logout_all(
    *,
    user: User,
) -> None:
    """
    Logout the user from every device.

    Every outstanding refresh token belonging to the user
    will be blacklisted.

    Existing access tokens remain valid until they expire.
    """

    outstanding_tokens = (
        OutstandingToken.objects
        .filter(user=user)
    )

    for token in outstanding_tokens:

        BlacklistedToken.objects.get_or_create(
            token=token,
        )