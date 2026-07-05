"""
Reusable DRF throttles.

Each throttle represents a business capability rather than
a specific endpoint.

Throttle rates are configured in REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"].
"""

from __future__ import annotations

from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle


# =============================================================================
# Public
# =============================================================================


class PublicThrottle(AnonRateThrottle):
    """
    Generic throttle for public endpoints.
    """

    scope = "public"


# =============================================================================
# Authentication
# =============================================================================


class LoginThrottle(AnonRateThrottle):
    """
    Limit login attempts.
    """

    scope = "login"


class PasswordResetThrottle(AnonRateThrottle):
    """
    Limit password reset requests.

    Prevents password reset email abuse.
    """

    scope = "password_reset"


class EmailVerificationThrottle(AnonRateThrottle):
    """
    Limit email verification requests.
    """

    scope = "email_verification"


class RegistrationThrottle(AnonRateThrottle):
    """
    Limit account creation.
    """

    scope = "registration"


# =============================================================================
# Authenticated
# =============================================================================


class AuthenticatedThrottle(UserRateThrottle):
    """
    Generic authenticated user throttle.
    """

    scope = "authenticated"


class PasswordChangeThrottle(UserRateThrottle):
    """
    Limit password change attempts.
    """

    scope = "password_change"


class EmailChangeThrottle(UserRateThrottle):
    """
    Limit email change attempts.
    """

    scope = "email_change"