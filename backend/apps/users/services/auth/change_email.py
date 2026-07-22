"""
Email change service.

Responsibilities:
    - Request an email change.
    - Confirm an email change.

Business orchestration only.

This service does not:
    - Generate tokens directly.
    - Hash tokens.
    - Send SMTP emails.
"""
from __future__ import annotations

from urllib.parse import urlencode

from django.db import transaction

from apps.users.exceptions.authentication import (
    EmailAlreadyInUse,
)

from apps.users.models import User

from apps.users.selectors.user import (
    find_user_by_email,
)

from apps.users.services.tokens.email_change import (
    create_email_change_token,
    verify_email_change_token,
    consume_email_change_tokens,
)

from apps.users.tasks.emails import (
    send_email_change_verification_email,
)

from config.settings.components.auth import (
    FRONTEND_EMAIL_CHANGE_URL,
)


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def request_email_change(
    *,
    user: User,
    new_email: str,
    created_ip: str | None = None,
    user_agent: str = "",
) -> None:
    """
    Request an email address change.

    Workflow:

        - Ensure the new email is not already in use.
        - Consume previous unused email change tokens.
        - Create a new email change token.
        - Queue verification email.
    """

    new_email = new_email.lower().strip()

    if user.email.lower() == new_email:
        return

    if find_user_by_email(new_email):
        raise EmailAlreadyInUse(
            "An account with this email already exists."
        )

    consume_email_change_tokens(
        user=user,
    )

    result = create_email_change_token(
        user=user,
        new_email=new_email,
        created_ip=created_ip,
        user_agent=user_agent,
    )

    verification_url = _build_email_change_url(
        token=result.raw_token,
    )

    transaction.on_commit(
        lambda: send_email_change_verification_email.delay(
            recipient=new_email,
            full_name=user.full_name,
            verification_url=verification_url,
        )
    )


@transaction.atomic
def confirm_email_change(
    *,
    raw_token: str,
) -> User:
    """
    Confirm an email change.

    Workflow:

        - Verify token.
        - Update user's email.
        - Mark email verified.
        - Consume all outstanding tokens.
    """

    token = verify_email_change_token(
        raw_token=raw_token,
    )

    user = token.user

    user.email = token.new_email
    user.email_verified = True

    user.save(
        update_fields=[
            "email",
            "email_verified",
        ]
    )

    consume_email_change_tokens(
        user=user,
    )

    return user


# =============================================================================
# Helpers
# =============================================================================


def _build_email_change_url(
    *,
    token: str,
) -> str:
    """
    Build frontend confirmation URL.
    """

    return (
        f"{FRONTEND_EMAIL_CHANGE_URL}"
        f"?{urlencode({'token': token})}"
    )