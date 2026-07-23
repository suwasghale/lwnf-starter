"""
Serializer for deleting the authenticated user's account.
"""

from __future__ import annotations

from rest_framework import serializers


class DeleteAccountSerializer(serializers.Serializer):
    """
    Confirm account deletion by requiring the current password.
    """

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )