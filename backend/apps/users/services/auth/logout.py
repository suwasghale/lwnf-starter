"""
Logout service.
"""

from __future__ import annotations

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.exceptions.authentication import (
    AuthenticationTokenInvalid,
)


def logout(
    *,
    refresh: str,
) -> None:
    """
    Blacklist a refresh token.
    """

    try:
        token = RefreshToken(refresh)

        token.blacklist()

    except TokenError as exc:
        raise AuthenticationTokenInvalid() from exc