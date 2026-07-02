"""
===============================================================================
LWNF Backend - User Exceptions
===============================================================================

Custom exceptions for the Users application.

===============================================================================
"""


# =============================================================================
# Base Exception
# =============================================================================


class LWNFException(Exception):
    """
    Base exception for the LWNF project.

    Every custom application exception should inherit from this class.
    """

    default_message = "An unexpected application error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


# =============================================================================
# User Exceptions
# =============================================================================


class UserException(LWNFException):
    """Base exception for user-related errors."""


class UserNotFound(UserException):
    default_message = "User does not exist."


class UserAlreadyExists(UserException):
    default_message = "User already exists."


class UserInactive(UserException):
    default_message = "User account is inactive."


class UserSuspended(UserException):
    default_message = "User account has been suspended."


class UserArchived(UserException):
    default_message = "User account has been archived."


# =============================================================================
# Authentication Exceptions
# =============================================================================


class AuthenticationException(LWNFException):
    """Base exception for authentication failures."""


class InvalidCredentials(AuthenticationException):
    default_message = "Invalid email or password."


class InvalidOTP(AuthenticationException):
    default_message = "Invalid one-time password."


class OTPExpired(AuthenticationException):
    default_message = "One-time password has expired."


class InvalidToken(AuthenticationException):
    default_message = "Authentication token is invalid."


class EmailNotVerified(AuthenticationException):
    default_message = "Email address has not been verified."


# =============================================================================
# Registration Exceptions
# =============================================================================


class RegistrationException(LWNFException):
    """Base exception for registration failures."""


class EmailAlreadyRegistered(RegistrationException):
    default_message = "Email address is already registered."


class UsernameAlreadyExists(RegistrationException):
    default_message = "Username is already in use."


class PhoneNumberAlreadyExists(RegistrationException):
    default_message = "Phone number is already registered."


# =============================================================================
# Permission Exceptions
# =============================================================================


class PermissionException(LWNFException):
    """Base exception for authorization failures."""


class PermissionDenied(PermissionException):
    default_message = "You do not have permission to perform this action."


class AccountLocked(PermissionException):
    default_message = "Account has been temporarily locked."