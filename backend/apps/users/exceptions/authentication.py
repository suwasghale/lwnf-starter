"""
===============================================================================
LWNF Backend - Authentication Exceptions
===============================================================================

Exceptions related to authentication and security.
===============================================================================
"""

from core.exceptions import LWNFException


class AuthenticationException(LWNFException):
    """Base exception for authentication failures."""


# =============================================================================
# Credentials
# =============================================================================

class InvalidCredentials(AuthenticationException):
    default_message = "Invalid email or password."


class EmailNotVerified(AuthenticationException):
    default_message = "Email address has not been verified."


# =============================================================================
# OTP
# =============================================================================

class InvalidOTP(AuthenticationException):
    default_message = "Invalid one-time password."


class OTPExpired(AuthenticationException):
    default_message = "One-time password has expired."


# =============================================================================
# Email Verification
# =============================================================================

class EmailVerificationTokenInvalid(AuthenticationException):
    default_message = "Email verification link is invalid."


class EmailVerificationTokenExpired(AuthenticationException):
    default_message = "Email verification link has expired."


class EmailAlreadyVerified(AuthenticationException):
    default_message = "Email address has already been verified."


# =============================================================================
# Password Reset
# =============================================================================

class PasswordResetTokenInvalid(AuthenticationException):
    default_message = "Password reset link is invalid."


class PasswordResetTokenExpired(AuthenticationException):
    default_message = "Password reset link has expired."


# =============================================================================
# Authentication Token (JWT/API)
# =============================================================================

class AuthenticationTokenInvalid(AuthenticationException):
    default_message = "Authentication token is invalid."


class AuthenticationTokenExpired(AuthenticationException):
    default_message = "Authentication token has expired."