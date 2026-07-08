"""
Serializers for the Address model.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Full address representation, used for read, create, and update.
    """

    class Meta:
        model = Address
        fields = (
            "id",
            "address_type",
            "label",
            "street_address",
            "address_line_2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
