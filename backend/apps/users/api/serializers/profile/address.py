"""
Serializer for user addresses.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    User address serializer.
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
        )

        read_only_fields = fields