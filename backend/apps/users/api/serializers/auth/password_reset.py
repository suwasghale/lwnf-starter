"""
Serializers for password reset.

Serializers are responsible only for:

- validating incoming request data
- normalizing input
- running Django password validators

They NEVER contain business logic.
"""

from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


# =============================================================================
# Password Reset Request
# =============================================================================


class PasswordResetRequestSerializer(
    serializers.Serializer,
):
    """
    Serializer used to request a password reset email.
    """

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    def validate_email(
        self,
        value: str,
    ) -> str:
        """
        Normalize email.

        User existence is intentionally NOT checked here.
        That belongs to the service layer to avoid user enumeration.
        """
        return value.strip().lower()


# =============================================================================
# Password Reset Verification
# =============================================================================


class PasswordResetVerifySerializer(
    serializers.Serializer,
):
    """
    Serializer used to verify a password reset token.
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
        """
        Normalize token.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Token is required."
            )

        return value


# =============================================================================
# Password Reset Confirmation
# =============================================================================


class PasswordResetConfirmSerializer(
    serializers.Serializer,
):
    """
    Serializer used to reset a password.
    """

    token = serializers.CharField(
        required=True,
        trim_whitespace=True,
        max_length=512,
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={
            "input_type": "password",
        },
    )

    password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        trim_whitespace=False,
        style={
            "input_type": "password",
        },
    )

    def validate_token(
        self,
        value: str,
    ) -> str:
        """
        Normalize token.
        """
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Token is required."
            )

        return value

    def validate(
        self,
        attrs: dict,
    ) -> dict:
        """
        Validate password confirmation.
        """

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