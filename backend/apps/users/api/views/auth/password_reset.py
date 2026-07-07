"""
Password reset API views.

Views are intentionally thin.

Responsibilities:

- validate request data
- call services
- return standardized responses

Business logic belongs to services.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import AllowAny

from ...serializers.auth.registration import RegistrationSerializer

from core.api.base import BaseAPIView

from core.api.schemas import (
    success_schema,
    bad_request_schema,
    too_many_requests_schema,
)

from core.api.throttles import PasswordResetThrottle

from apps.users.api.serializers.auth.password_reset import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
)

from apps.users.services.auth.password_reset import (
    request_password_reset,
    reset_password,
    verify_password_reset_token,
)


# =============================================================================
# Request Password Reset
# =============================================================================

@extend_schema(
    tags=["Authentication"],
    request=PasswordResetRequestSerializer,
    responses={
        200: success_schema(
            description="Password reset email requested.",
        ),
        400: bad_request_schema(),
        429: too_many_requests_schema(),
    },
)
class PasswordResetRequestAPIView(BaseAPIView):
    """
    Request a password reset email.
    """

    permission_classes = (AllowAny,)
    throttle_classes = (PasswordResetThrottle,)

    serializer_class = PasswordResetRequestSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        request_password_reset(
            email=serializer.validated_data["email"],
            created_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get(
                "HTTP_USER_AGENT",
                "",
            ),
        )

        return success_response(
            message=(
                "If an account exists, a password reset email has been sent."
            ),
        )


# =============================================================================
# Verify Token
# =============================================================================


@extend_schema(
    tags=["Authentication"],
    request=PasswordResetRequestSerializer,
    responses={
        200: success_schema(
            description="Password reset token is valid.",
        ),
        400: bad_request_schema(),
        429: too_many_requests_schema(),
    },
)


class PasswordResetVerifyAPIView(BaseAPIView):
    """
    Verify a password reset token.
    """

    permission_classes = (AllowAny,)

    serializer_class = PasswordResetVerifySerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        verify_password_reset_token(
            raw_token=serializer.validated_data["token"],
        )

        return success_response(
            message="Token is valid.",
        )


# =============================================================================
# Reset Password
# =============================================================================


@extend_schema(
    tags=["Authentication"],
    request=PasswordResetRequestSerializer,
    responses={
        200: success_schema(
            description="Password reset successfully.",
        ),
        400: bad_request_schema(),
        429: too_many_requests_schema(),
    },
)


class PasswordResetConfirmAPIView(BaseAPIView):
    """
    Reset a user's password.
    """

    permission_classes = (AllowAny,)

    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        reset_password(
            raw_token=serializer.validated_data["token"],
            new_password=serializer.validated_data["password"],
        )

        return success_response(
            message="Password has been reset successfully.",
        )