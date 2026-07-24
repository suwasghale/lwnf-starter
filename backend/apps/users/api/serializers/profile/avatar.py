"""
Serializer for avatar uploads.
"""

from __future__ import annotations

from rest_framework import serializers
from django.core.files.uploadedfile import UploadedFile

from apps.users.constants import (
    AVATAR_MAX_FILE_SIZE,
    AVATAR_ALLOWED_CONTENT_TYPES,
)


class AvatarUploadSerializer(serializers.Serializer):
    """
    Validate an uploaded avatar image.
    """

    avatar = serializers.ImageField(
        required=True,
    )

    def validate_avatar(
    self,
    value: UploadedFile,
    ) -> UploadedFile:
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

        if value.content_type not in AVATAR_ALLOWED_CONTENT_TYPES:
            raise serializers.ValidationError(
                "Supported image formats are JPG, JPEG, PNG and WebP."
            )

        return value