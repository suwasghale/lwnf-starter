from rest_framework import serializers

from apps.users.models import User

from apps.users.api.serializers.profile.profile import (
    ProfileSerializer,
)
from apps.users.api.serializers.profile.address import (
    AddressSerializer,
)

class CurrentUserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    profile = ProfileSerializer(
        read_only=True,
    )

    addresses = AddressSerializer(
        many=True,
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
            "profile",
            "addresses",
        )