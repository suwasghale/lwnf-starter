"""
Email verification services.

Business logic for:

- creating verification tokens
- sending verification emails
- verifying email tokens
- resending verification emails

Views should never contain this logic.
"""

from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.users.models import (
    User,
)
from apps.users.models.tokens.email_verification import (
    EmailVerificationToken, )

from apps.users.selectors.auth.email_verification import (
    find_verification_token,
)
from apps.users.exceptions.authentication import (
    EmailAlreadyVerified,
    EmailVerificationTokenExpired,
    EmailVerificationTokenInvalid,
)

from core.security.tokens import (
    generate_hashed_token,
    hash_token,
)

from apps.users.tasks.email import (
    send_email_verification_email,
)

from apps.users.utils.urls import (
    build_email_verification_url,
)


@transaction.atomic
def create_email_verification(
    *,
    user: User,
    created_ip: str | None,
    user_agent: str,
) -> None:
    """
    Create a fresh verification token and send email.
    """

    EmailVerificationToken.objects.invalidate_user_tokens(
        user=user,
    )

    raw_token, token_hash = generate_hashed_token()

    expires_at = (
        timezone.now()
        + timedelta(
            hours=settings.EMAIL_VERIFICATION_TOKEN_LIFETIME_HOURS,
        )
    )

    EmailVerificationToken.objects.create_verification_token(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at,
        created_ip=created_ip,
        user_agent=user_agent,
    )

    verification_url = build_email_verification_url(
        token=raw_token,
    )
    print("Creating verification email...")
    
    result = send_email_verification_email.delay(
        recipient=user.email,
        full_name=user.full_name,
        verification_url=verification_url,
    )

    print(result.id)


@transaction.atomic
def verify_email(
    *,
    raw_token: str,
) -> User:
    """
    Verify a user's email.
    """

    token_hash = hash_token(raw_token)

    token = find_verification_token(
        token_hash=token_hash,
    )

    if token is None:
        raise EmailVerificationTokenInvalid()

    if token.used_at is not None:
        raise EmailVerificationTokenInvalid()

    if token.expires_at <= timezone.now():
        raise EmailVerificationTokenExpired()

    if token.user.is_verified:
        raise EmailAlreadyVerified()

    token.user.is_verified = True

    token.user.save(
        update_fields=[
            "is_verified",
        ],
    )

    token.used_at = timezone.now()

    token.save(
        update_fields=[
            "used_at",
        ],
    )

    return token.user


@transaction.atomic
def resend_email_verification(
    *,
    user: User,
    created_ip: str | None,
    user_agent: str,
) -> None:
    """
    Send a fresh verification email.
    """

    if user.is_verified:
        return

    create_email_verification(
        user=user,
        created_ip=created_ip,
        user_agent=user_agent,
    )