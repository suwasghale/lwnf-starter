"""
Selectors related to the Profile model.
"""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from apps.users.models import Profile


def get_profile_by_user(user_id: UUID) -> Profile:
    """
    Return profile for a given user.
    """
    return (
        Profile.objects
        .select_related("user")
        .get(user_id=user_id)
    )


def find_profile_by_user(user_id: UUID) -> Profile | None:
    """
    Return profile or None.
    """
    return (
        Profile.objects
        .select_related("user")
        .filter(user_id=user_id)
        .first()
    )


def list_profiles() -> QuerySet[Profile]:
    """
    Return all profiles.
    """
    return (
        Profile.objects
        .select_related("user")
        .order_by("-created_at")
    )