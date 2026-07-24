"""
Account avatar update service.
"""

from __future__ import annotations

import uuid

from django.db import transaction

from apps.users.models import User

from apps.users.selectors.profile import (
    get_profile_by_user,
)

from core.storage.images import (
    process_image,
)

from apps.users.constants import (
    AVATAR_UPLOAD_PATH,
    DEFAULT_AVATAR,
)


# =============================================================================
# Public API
# =============================================================================


@transaction.atomic
def update_avatar(
    *,
    user: User,
    avatar,
) -> User:
    """
    Update the authenticated user's avatar.

    Workflow

        1. Load profile.
        2. Delete previous avatar.
        3. Process uploaded image.
        4. Upload to Cloudflare R2.
        5. Save profile.

    Returns

        Updated user instance.
    """

    profile = get_profile_by_user(
        user_id=user.id,
    )

    # -------------------------------------------------------------------------
    # Remove previous avatar
    # -------------------------------------------------------------------------

    if (
        profile.avatar
        and profile.avatar.name
        and profile.avatar.name != DEFAULT_AVATAR
    ):
        profile.avatar.delete(
            save=False,
        )

    # -------------------------------------------------------------------------
    # Process image
    # -------------------------------------------------------------------------

    processed_image = process_image(
        image_file=avatar,
    )

    # -------------------------------------------------------------------------
    # Build filename
    # -------------------------------------------------------------------------

    filename = (
        f"{AVATAR_UPLOAD_PATH}/"
        f"{user.id}/"
        f"{uuid.uuid4().hex}.webp"
    )

    # -------------------------------------------------------------------------
    # Upload
    # -------------------------------------------------------------------------

    profile.avatar.save(
        filename,
        processed_image,
        save=False,
    )

    profile.save(
        update_fields=[
            "avatar",
        ],
    )

    return user