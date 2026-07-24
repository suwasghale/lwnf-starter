"""
Serializer for updating the authenticated user's profile.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.choices import GenderChoices


class UpdateProfileSerializer(serializers.Serializer):
    """
    Partial update of the authenticated user's account.
    """

    # ------------------------------------------------------------------
    # User fields
    # ------------------------------------------------------------------

    first_name = serializers.CharField(
        required=False,
        max_length=150,
    )

    last_name = serializers.CharField(
        required=False,
        max_length=150,
    )

    # ------------------------------------------------------------------
    # Profile fields
    # ------------------------------------------------------------------

    gender = serializers.ChoiceField(
        required=False,
        choices=GenderChoices.choices,
    )

    date_of_birth = serializers.DateField(
        required=False,
    )

    nationality = serializers.CharField(
        required=False,
        max_length=2,
    )

    phone_number = serializers.CharField(
        required=False,
        max_length=32,
    )

    biography = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    preferred_language = serializers.CharField(
        required=False,
        max_length=10,
    )

    timezone = serializers.CharField(
        required=False,
        max_length=100,
    )

    def validate(self, attrs):
        """
        Ensure at least one field is supplied.
        """

        if not attrs:
            raise serializers.ValidationError(
                "At least one field must be provided."
            )

        return attrs