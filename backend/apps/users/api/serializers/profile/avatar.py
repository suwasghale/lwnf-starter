"""
Serializer for avatar uploads.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.constants import (
    AVATAR_MAX_FILE_SIZE,
    ALLOWED_AVATAR_CONTENT_TYPES,
)


class AvatarUploadSerializer(serializers.Serializer):
    """
    Validate an uploaded avatar image.
    """

    avatar = serializers.ImageField(
        required=True,
    )

    def validate_avatar(self, value):
        """
        Validate uploaded avatar.
        """

        # ---------------------------------------------------------------------
        # Maximum file size
        # ---------------------------------------------------------------------

        if value.size > AVATAR_MAX_FILE_SIZE:
            raise serializers.ValidationError(
                (
                    f"Avatar must be smaller than "
                    f"{AVATAR_MAX_FILE_SIZE // (1024 * 1024)} MB."
                )
            )

        # ---------------------------------------------------------------------
        # Allowed MIME types
        # ---------------------------------------------------------------------

        if value.content_type not in ALLOWED_AVATAR_CONTENT_TYPES:
            raise serializers.ValidationError(
                "Only JPG, JPEG, PNG and WebP images are allowed."
            )

        return value