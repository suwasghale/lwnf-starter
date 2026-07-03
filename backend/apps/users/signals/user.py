"""
Signal handlers for the User model.

Signals should remain lightweight and delegate business logic
to the service layer.

Responsibilities:
- React to domain events.
- Delegate work to services.
- Never contain business logic.
"""

from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import User
from apps.users.services.profile import (
    create_profile_for_user,
    update_profile_for_user,
)


@receiver(post_save, sender=User)
def handle_user_created(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs,
) -> None:
    """
    Automatically create a profile when a new user is created.
    """

    if not created:
        return

    create_profile_for_user(instance)


@receiver(post_save, sender=User)
def handle_user_updated(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs,
) -> None:
    """
    React to user updates.

    The actual business logic lives in the service layer.
    """

    if created:
        return

    update_profile_for_user(instance)