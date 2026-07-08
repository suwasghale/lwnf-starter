"""
Serializers for the Profile model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.constants import BIOGRAPHY_MAX_LENGTH
from apps.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Full profile representation, used for both read and update.
    """

    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "avatar",
            "gender",
            "date_of_birth",
            "age",
            "phone_number",
            "biography",
            "preferred_language",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "age", "created_at", "updated_at")

    def validate_biography(self, value: str) -> str:
        if len(value) > BIOGRAPHY_MAX_LENGTH:
            raise serializers.ValidationError(
                f"Biography must be at most {BIOGRAPHY_MAX_LENGTH} characters."
            )

        return value
