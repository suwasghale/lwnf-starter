"""
Account-related exceptions.
"""

from __future__ import annotations

from core.exceptions.base import LWNFException


class InvalidPassword(LWNFException):
    """
    Raised when the supplied password is incorrect.
    """

    default_message = "Current password is incorrect."


class AccountDeleted(LWNFException):
    default_message = "This account has been deleted."
    

class AccountDisabled(LWNFException):
    default_message = "This account has been disabled."