"""
Selectors related to the Address model.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.users.models import Address


def get_default_address(user_id: UUID) -> Address:
    """
    Return the default address for a user.

    Raises:
        Address.DoesNotExist
    """
    return (
        Address.objects
        .select_related("user")
        .get(
            user_id=user_id,
            is_default=True,
        )
    )


def find_default_address(user_id: UUID) -> Address | None:
    """
    Return the default address or None.
    """
    return (
        Address.objects
        .select_related("user")
        .filter(
            user_id=user_id,
            is_default=True,
        )
        .first()
    )


def list_user_addresses(user_id: UUID) -> QuerySet[Address]:
    """
    Return every address belonging to a user.
    """
    return (
        Address.objects
        .select_related("user")
        .filter(user_id=user_id)
        .order_by(
            "-is_default",
            "-created_at",
        )
    )


def list_default_addresses() -> QuerySet[Address]:
    """
    Return every default address.
    """
    return (
        Address.objects
        .select_related("user")
        .filter(is_default=True)
    )