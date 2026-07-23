"""
Account-related exceptions.
"""

from __future__ import annotations

from core.exceptions.base import BusinessLogicException


class InvalidPassword(BusinessLogicException):
    """
    Raised when the supplied password is incorrect.
    """

    default_message = "Current password is incorrect."