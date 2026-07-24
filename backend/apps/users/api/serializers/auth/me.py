"""
Serializer for the authenticated user.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source="full_name")

    avatar = serializers.ImageField(
        source="profile.avatar",
        read_only=True,
    )

    biography = serializers.CharField(
        source="profile.biography",
        read_only=True,
    )

    phone_number = serializers.CharField(
        source="profile.phone_number",
        read_only=True,
    )

    gender = serializers.CharField(
        source="profile.gender",
        read_only=True,
    )

    date_of_birth = serializers.DateField(
        source="profile.date_of_birth",
        read_only=True,
    )

    nationality = serializers.CharField(
        source="profile.nationality",
        read_only=True,
    )

    preferred_language = serializers.CharField(
        source="profile.preferred_language",
        read_only=True,
    )

    timezone = serializers.CharField(
        source="profile.timezone",
        read_only=True,
    )

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_verified",
            "is_staff",
            "is_active",
            "date_joined",

            # profile
            "avatar",
            "phone_number",
            "gender",
            "date_of_birth",
            "nationality",
            "biography",
            "preferred_language",
            "timezone",
        )