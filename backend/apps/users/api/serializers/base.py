"""
Base serializers shared across the Users API.

These classes provide reusable validation helpers only.

They must NEVER contain business logic.
"""

from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


# =============================================================================
# Base Serializer
# =============================================================================


class BaseSerializer(serializers.Serializer):
    """
    Base serializer for the Users application.
    """

    @staticmethod
    def normalize_email(
        email: str,
    ) -> str:
        """
        Normalize an email address.
        """
        return email.strip().lower()


# =============================================================================
# Email Serializer
# =============================================================================


class EmailSerializer(BaseSerializer):
    """
    Reusable serializer containing a normalized email field.
    """

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        return self.normalize_email(value)


# =============================================================================
# Token Serializer
# =============================================================================


class TokenSerializer(BaseSerializer):
    """
    Reusable serializer containing a token field.
    """

    token = serializers.CharField(
        required=True,
        trim_whitespace=True,
        max_length=512,
    )

    def validate_token(
        self,
        value: str,
    ) -> str:
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Token is required."
            )

        return value


# =============================================================================
# Password Confirmation Serializer
# =============================================================================


class PasswordConfirmationSerializer(TokenSerializer):
    """
    Reusable serializer containing:

    - token
    - password
    - password confirmation
    """

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={
            "input_type": "password",
        },
    )

    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={
            "input_type": "password",
        },
    )

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]

        if password != password_confirm:
            raise serializers.ValidationError(
                {
                    "password_confirm": (
                        "Passwords do not match."
                    )
                }
            )

        validate_password(password)

        return attrs