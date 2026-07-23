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