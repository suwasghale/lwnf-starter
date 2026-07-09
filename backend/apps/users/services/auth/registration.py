"""
Business service responsible for user registration.
"""

from __future__ import annotations

from urllib.parse import urlencode

from django.db import transaction
from django.utils import timezone

from typing import Any

from apps.users.exceptions.registration import (
    EmailAlreadyRegistered,
)
from apps.users.models import (
    Profile,
    User,
)
from apps.users.models.tokens import (
    EmailVerificationToken,
)
from apps.users.selectors.user import (
    exists_user_by_email,
)
from apps.users.tasks.email import (
    send_email_verification_email,
)

from core.security.tokens import (
    generate_hashed_token,
)

from config.settings.components.auth import (
    EMAIL_VERIFICATION_TOKEN_LIFETIME,
    FRONTEND_EMAIL_VERIFICATION_URL,
)


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def register_user(
    *,
    data: dict[str, Any],
    created_ip: str | None = None,
    user_agent: str = "",
) -> User:
    """
    Register a new user.

    Workflow:

        - Ensure email is unique.
        - Create user.
        - Create profile.
        - Generate verification token.
        - Persist hashed token.
        - Queue verification email.

    Returns:
        Newly created User.

    Raises:
        EmailAlreadyRegistered
    """
    
    email = str(data["email"])
    password = str(data["password"])
    first_name = str(data.get("first_name", ""))
    last_name = str(data.get("last_name", ""))

    if exists_user_by_email(email=email):
        raise EmailAlreadyRegistered()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
        is_verified=False,
    )

    # Profile.objects.create(
    #     user=user,
    # )

    raw_token, token_hash = generate_hashed_token()

    expires_at = (
        timezone.now()
        + EMAIL_VERIFICATION_TOKEN_LIFETIME
    )

    # EmailVerificationToken.objects.invalidate_user_tokens(
    #     user=user,
    # )

    EmailVerificationToken.objects.create_verification_token(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
        created_ip=created_ip,
        user_agent=user_agent,
    )

    verification_url = _build_verification_url(
        token=raw_token,
    )

    transaction.on_commit(
        lambda: send_email_verification_email.delay(
            recipient=user.email,
            full_name=user.full_name,
            verification_url=verification_url,
        )
    )

    return user


# =============================================================================
# Internal Helpers
# =============================================================================


def _build_verification_url(
    *,
    token: str,
) -> str:
    """
    Build the frontend verification URL.
    """

    return (
        f"{FRONTEND_EMAIL_VERIFICATION_URL}"
        f"?{urlencode({'token': token})}"
    )