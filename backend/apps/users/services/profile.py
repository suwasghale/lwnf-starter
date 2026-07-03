"""
Business logic related to user profiles.
"""

from __future__ import annotations

from apps.users.models import Profile, User


def create_profile_for_user(user: User) -> Profile:
    """
    Create a profile for the given user.

    If a profile already exists, return it.
    """

    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def update_profile_for_user(user: User) -> Profile:
    """
    Handle profile updates after a user is saved.

    This is intentionally lightweight for now and serves as
    an extension point for future business logic.
    """

    profile, _ = Profile.objects.get_or_create(user=user)

    profile.save(
        update_fields=[
            "updated_at",
        ]
    )

    return profile