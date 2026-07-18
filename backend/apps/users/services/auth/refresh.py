"""
JWT refresh service.
"""

from __future__ import annotations

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.exceptions.authentication import (
    AuthenticationTokenInvalid,
)


def refresh_access_token(
    *,
    refresh: str,
) -> dict[str, str]:
    """
    Validate refresh token and issue a new access token.
    """

    try:
        refresh_token = RefreshToken(refresh)

    except TokenError as exc:
        raise AuthenticationTokenInvalid() from exc

    return {
        "access": str(refresh_token.access_token),
    }