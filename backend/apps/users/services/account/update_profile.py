"""
Account profile update service.
"""

from __future__ import annotations

from django.db import transaction

from apps.users.models import User

from apps.users.selectors.profile import (
    get_profile_by_user,
)


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def update_profile(
    *,
    user: User,
    validated_data: dict,
) -> User:
    """
    Update the authenticated user's account.

    This updates both the User and Profile models inside
    a single database transaction.
    """

    profile = get_profile_by_user(
        user_id=user.id,
    )

    # -------------------------------------------------------------------------
    # User fields
    # -------------------------------------------------------------------------

    user_fields = []

    if "first_name" in validated_data:
        user.first_name = validated_data["first_name"]
        user_fields.append("first_name")

    if "last_name" in validated_data:
        user.last_name = validated_data["last_name"]
        user_fields.append("last_name")

    if user_fields:
        user.save(
            update_fields=user_fields,
        )

    # -------------------------------------------------------------------------
    # Profile fields
    # -------------------------------------------------------------------------

    profile_fields = []

    profile_mapping = {
        "gender": "gender",
        "date_of_birth": "date_of_birth",
        "nationality": "nationality",
        "phone_number": "phone_number",
        "biography": "biography",
        "preferred_language": "preferred_language",
        "timezone": "timezone",
    }

    for serializer_field, model_field in profile_mapping.items():

        if serializer_field in validated_data:
            setattr(
                profile,
                model_field,
                validated_data[serializer_field],
            )

            profile_fields.append(model_field)

    if profile_fields:
        profile.save(
            update_fields=profile_fields,
        )

    return user