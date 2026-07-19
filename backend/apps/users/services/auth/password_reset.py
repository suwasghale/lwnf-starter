"""
Business services for password reset.

This module orchestrates the complete password reset workflow.

Responsibilities:
    - Generate secure password reset tokens.
    - Persist hashed tokens.
    - Invalidate previous tokens.
    - Send password reset emails.
    - Verify password reset tokens.
    - Reset user passwords.

Services contain business logic only.
"""

from __future__ import annotations

from urllib.parse import urlencode

from django.db import transaction
from django.utils import timezone

from apps.users.exceptions.authentication import (
    PasswordResetTokenInvalid,)
from apps.users.models import User
from apps.users.models.tokens import PasswordResetToken
from apps.users.selectors.auth.password_reset import (
    get_valid_password_reset_token,
)
from apps.users.selectors.user import (
    find_user_by_email,
)
from apps.users.services.user import (
    change_password,
)
from apps.users.tasks.emails import (
    send_password_reset_email,
)

from config.settings.components.auth import (
    FRONTEND_PASSWORD_RESET_URL,
    PASSWORD_RESET_TOKEN_LIFETIME,
)

from core.security.tokens import (
    generate_hashed_token,
    hash_token,
)


# =============================================================================
# Public API
# =============================================================================


def request_password_reset(
    *,
    email: str,
    created_ip: str | None = None,
    user_agent: str = "",
) -> None:
    """
    Request a password reset.

    Workflow:

        - Find user.
        - Ignore unknown accounts.
        - Generate a secure token.
        - Invalidate previous tokens.
        - Store only the hashed token.
        - Queue the password reset email after commit.

    Notes:
        This method intentionally does not reveal whether
        the email address exists.
    """

    user = find_user_by_email(email)

    if user is None:
        return

    raw_token, token_hash = generate_hashed_token()

    expires_at = (
        timezone.now()
        + PASSWORD_RESET_TOKEN_LIFETIME
    )

    with transaction.atomic():

        _invalidate_existing_tokens(
            user=user,
        )

        PasswordResetToken.objects.create_password_reset_token(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at,
            created_ip=created_ip,
            user_agent=user_agent,
        )

        reset_url = _build_password_reset_url(
            token=raw_token,
        )

        transaction.on_commit(
            lambda: send_password_reset_email.delay(
                recipient=user.email,
                full_name=user.full_name,
                reset_url=reset_url,
            )
        )


# =============================================================================
# Verification
# =============================================================================


def verify_password_reset_token(
    *,
    raw_token: str,
) -> PasswordResetToken:
    """
    Verify that a password reset token is valid.

    Does not mutate the database.

    Raises:
        InvalidToken
    """

    return _get_valid_token(
        raw_token=raw_token,
    )


# =============================================================================
# Password Reset
# =============================================================================


@transaction.atomic
def reset_password(
    *,
    raw_token: str,
    new_password: str,
) -> User:
    """
    Reset a user's password.

    Workflow:

        - Verify token.
        - Change password.
        - Consume current token.
        - Invalidate every remaining token.

    Raises:
        InvalidToken
    """

    token = _get_valid_token(
        raw_token=raw_token,
    )

    user = token.user

    change_password(
        user=user,
        password=new_password,
    )

    token.consume()

    _invalidate_existing_tokens(
        user=user,
    )

    return user


# =============================================================================
# Internal Helpers
# =============================================================================


def _invalidate_existing_tokens(
    *,
    user: User,
) -> None:
    """
    Consume every unused password reset token
    belonging to the user.
    """

    PasswordResetToken.objects.invalidate_user_tokens(
        user=user,
    )


def _build_password_reset_url(
    *,
    token: str,
) -> str:
    """
    Build the frontend password reset URL.
    """

    return (
        f"{FRONTEND_PASSWORD_RESET_URL}"
        f"?{urlencode({'token': token})}"
    )


def _get_valid_token(
    *,
    raw_token: str,
) -> PasswordResetToken:
    """
    Return a valid password reset token.

    Raises:
        PasswordResetTokenInvalid
    """

    token_hash = hash_token(raw_token)

    try:
        return get_valid_password_reset_token(
            token_hash=token_hash,
        )

    except PasswordResetToken.DoesNotExist as exc:
        raise PasswordResetTokenInvalid(
            "Password reset token is invalid or has expired."
        ) from exc