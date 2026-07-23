"""
Business service responsible for user authentication.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.users.models import User

from apps.users.selectors.user import (
    find_user_by_email,
)

from apps.users.exceptions.authentication import (
    InvalidCredentials,
)

from apps.users.exceptions.account import (
    AccountDeleted,
    AccountDisabled,
)

from core.exceptions import LWNFException

from apps.users.exceptions.authentication import (
    EmailNotVerified,
)

from apps.users.services.auth.account_validation import (
    validate_account,
)

from apps.users.services.auth.jwt import (
    TokenPair,
    create_token_pair,
)


# =============================================================================
# DTO
# =============================================================================


@dataclass(slots=True)
class LoginResult:
    """
    Successful authentication result.
    """

    user: User

    tokens: TokenPair


# =============================================================================
# Public API
# =============================================================================


def login(
    *,
    email: str,
    password: str,
) -> LoginResult:
    """
    Authenticate a user.

    Workflow

        1. Find account.
        2. Verify password.
        3. Validate account status.
        4. Issue JWT tokens.

    Raises

        InvalidCredentials
        InactiveAccount
        EmailNotVerified
    """

    user = find_user_by_email(
        email=email,
    )

    if user is None:
        raise InvalidCredentials()
    
    if user.deleted_at is not None:
        print("ACCOUNT DELETED BRANCH")

        try:
            raise AccountDeleted()
        except Exception as e:
            print(type(e))
            print(isinstance(e, LWNFException))
            print(isinstance(e, Exception))
            raise

    if not user.is_active:
        raise AccountDisabled()

    if not user.is_verified:
        raise EmailNotVerified()

    if not user.check_password(password):
        raise InvalidCredentials()

    validate_account(
        user=user,
    )

    tokens = create_token_pair(
        user=user,
    )

    return LoginResult(
        user=user,
        tokens=tokens,
    )