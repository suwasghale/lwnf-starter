"""
===============================================================================
LWNF Backend - Permission Exceptions
===============================================================================

Exceptions related to authorization.
===============================================================================
"""

from common.exceptions import LWNFException


class PermissionException(LWNFException):
    """Base exception for authorization failures."""


class PermissionDenied(PermissionException):
    default_message = "You do not have permission to perform this action."


class AccountLocked(PermissionException):
    default_message = "Account has been temporarily locked."