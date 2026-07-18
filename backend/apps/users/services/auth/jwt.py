"""
JWT authentication services.

Business logic related to JWT tokens.

Responsibilities:

- issue token pair
- refresh access tokens
- revoke refresh tokens
- blacklist tokens
- decode tokens

Views should never interact with SimpleJWT directly.
"""

from __future__ import annotations

from dataclasses import dataclass

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


# =============================================================================
# DTO
# =============================================================================


@dataclass(slots=True)
class TokenPair:
    """
    JWT token pair.
    """

    access: str
    refresh: str


# =============================================================================
# Public API
# =============================================================================


def create_token_pair(
    *,
    user: User,
) -> TokenPair:
    """
    Issue a fresh JWT token pair.

    Returns:
        TokenPair
    """

    refresh = RefreshToken.for_user(user)

    return TokenPair(
        access=str(refresh.access_token),
        refresh=str(refresh),
    )


def create_access_token(
    *,
    refresh_token: RefreshToken,
) -> str:
    """
    Create a new access token from a refresh token.
    """

    return str(
        refresh_token.access_token,
    )


def revoke_refresh_token(
    *,
    refresh_token: RefreshToken,
) -> None:
    """
    Blacklist a refresh token.

    Requires SimpleJWT blacklist app.
    """

    refresh_token.blacklist()