"""
Serializer for the authenticated user.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Serializer representing the currently authenticated user.
    """

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_verified",
            "is_staff",
            "is_active",
        )

        read_only_fields = fields