"""
Business logic for requesting a password reset.
"""

from __future__ import annotations

from django.db import transaction

from config.settings.env import env

from apps.users.selectors.user import (
    find_user_by_email,
)

from apps.users.services.tokens.password_reset import (
    create_password_reset_token,
    invalidate_password_reset_tokens,
)

from apps.users.tasks.emails import (
    send_password_reset_email,
)

from core.security.tokens import (
    build_frontend_url,
)


# =============================================================================
# Settings
# =============================================================================

FRONTEND_PASSWORD_RESET_URL = env(
    "FRONTEND_PASSWORD_RESET_URL",
)


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def forgot_password(
    *,
    email: str,
    created_ip: str | None = None,
    user_agent: str = "",
) -> None:
    """
    Request a password reset.

    Security:
        - Never reveal whether an account exists.
        - Ignore inactive accounts.
        - Invalidate previous unused tokens.
        - Issue a new password reset token.
        - Queue a password reset email.
    """
    
    print("INSIDE FORGOT PASSWORD SERVICE")

    user = find_user_by_email(
        email=email,
    )

    # -------------------------------------------------------------------------
    # Prevent email enumeration.
    # -------------------------------------------------------------------------

    if user is None or not user.is_active:
        return

    # -------------------------------------------------------------------------
    # Invalidate previous password reset tokens.
    # -------------------------------------------------------------------------

    invalidate_password_reset_tokens(
        user=user,
    )

    # -------------------------------------------------------------------------
    # Create a fresh password reset token.
    # -------------------------------------------------------------------------

    result = create_password_reset_token(
        user=user,
        created_ip=created_ip,
        user_agent=user_agent,
    )

    # -------------------------------------------------------------------------
    # Build frontend reset URL.
    # -------------------------------------------------------------------------

    reset_url = build_frontend_url(
        base_url=FRONTEND_PASSWORD_RESET_URL,
        token=result.raw_token,
    )

    # -------------------------------------------------------------------------
    # Queue password reset email.
    # -------------------------------------------------------------------------

    # send_password_reset_email.delay(
    #     recipient=user.email,
    #     full_name=user.full_name,
    #     reset_url=reset_url,
    # )
    
    print("========== BEFORE DELAY ==========")

    result = send_password_reset_email.delay(
        recipient=user.email,
        full_name=user.full_name,
        reset_url=reset_url,
    )

    print("TASK ID:", result.id)
    print("========== AFTER DELAY ==========")