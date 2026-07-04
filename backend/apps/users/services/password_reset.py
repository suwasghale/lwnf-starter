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

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.users.exceptions import (
    InvalidToken,
    UserNotFound,
)
from apps.users.models import User
from apps.users.models.tokens import PasswordResetToken
from apps.users.selectors.password_reset import (
    find_valid_password_reset_token,
)
from apps.users.selectors.user import (
    find_user_by_email,
)
from apps.users.services.user import (
    change_password,
)
from apps.users.tasks.email import (
    send_password_reset_email,
)

from core.security.tokens import (
    generate_hashed_token,
    hash_token,
)

from config.settings.components.auth import (
    PASSWORD_RESET_TOKEN_LIFETIME,
    FRONTEND_PASSWORD_RESET_URL,
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
        - Invalidate previous reset tokens.
        - Generate a new secure token.
        - Store only its hash.
        - Queue the email.
    """

    user = find_user_by_email(email)

    if user is None:
        return

    _invalidate_existing_tokens(
        user=user,
    )

    raw_token, token_hash = generate_hashed_token()

    expires_at = (
        timezone.now()
        + PASSWORD_RESET_TOKEN_LIFETIME
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

    send_password_reset_email.delay(
        recipient=user.email,
        full_name=user.full_name,
        reset_url=reset_url,
    )


# =============================================================================
# Internal Helpers
# =============================================================================


def _invalidate_existing_tokens(
    *,
    user: User,
) -> None:
    """
    Consume every existing password reset token.

    Only one active reset token should exist
    for a user at any time.
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

    Example:

        https://app.lwnf.org/reset-password?token=...
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
        InvalidToken
    """

    token_hash = hash_token(
        raw_token,
    )

    token = find_valid_password_reset_token(
        token_hash=token_hash,
    )

    if token is None:
        raise InvalidToken(
            "Password reset token is invalid or has expired."
        )

    return token