"""
Selectors related to the User model.

Selectors are responsible ONLY for reading data.

They never create, update or delete records.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.users.models import User


# =============================================================================
# Single Objects
# =============================================================================


def get_user_by_id(
    *,
    user_id: UUID,
) -> User:
    """
    Return a user by UUID.

    Raises:
        User.DoesNotExist
    """
    return (
        User.objects
        .select_related("profile")
        .get(pk=user_id)
    )


def find_user_by_email(
    *,
    email: str,
) -> User | None:
    """
    Return a user by email.

    Returns:
        User | None
    """
    return (
        User.objects
        .select_related("profile")
        .filter(email__iexact=email)
        .first()
    )


# =============================================================================
# Lists
# =============================================================================


def list_users() -> QuerySet[User]:
    """
    Return every user.
    """
    return (
        User.objects
        .select_related("profile")
        .order_by("-created_at")
    )


def list_active_users() -> QuerySet[User]:
    """
    Return active users.
    """
    return (
        User.objects
        .select_related("profile")
        .filter(is_active=True)
        .order_by("-created_at")
    )


def list_verified_users() -> QuerySet[User]:
    """
    Return verified users.
    """
    return (
        User.objects
        .select_related("profile")
        .filter(
            is_active=True,
            is_verified=True,
        )
        .order_by("-created_at")
    )


def list_staff_users() -> QuerySet[User]:
    """
    Return staff users.
    """
    return (
        User.objects
        .select_related("profile")
        .filter(is_staff=True)
        .order_by("email")
    )


# =============================================================================
# Boolean
# =============================================================================


def exists_user_by_email(
    *,
    email: str,
) -> bool:
    """
    Return whether a user exists with the given email.
    """
    return (
        User.objects
        .filter(email__iexact=email)
        .exists()
    )