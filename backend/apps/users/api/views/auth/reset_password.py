"""
Reset password API.

Responsibilities:
    - Validate request data.
    - Call password reset service.
    - Return HTTP response.

No business logic belongs here.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from apps.users.api.serializers.auth.reset_password import (
    ResetPasswordSerializer,
)

from apps.users.services.auth.reset_password import (
    reset_password,
)


class ResetPasswordAPIView(APIView):
    """
    Complete a password reset.
    """

    permission_classes = [AllowAny]

    authentication_classes = []

    serializer_class = ResetPasswordSerializer

    @extend_schema(
        tags=["Authentication"],
        summary="Reset password",
        description=(
            "Reset a user's password using a valid password reset token."
        ),
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(
                description="Password successfully updated.",
            ),
            400: OpenApiResponse(
                description="Invalid request.",
            ),
        },
        examples=[
            OpenApiExample(
                name="Reset password",
                value={
                    "token": "2KFJ7EnClpU67a4uOYgERqjF1PwUlqcu3nrPUFVk_5w",
                    "password": "MySecurePassword123!",
                    "password_confirm": "MySecurePassword123!",
                },
                request_only=True,
            ),
        ],
    )
    def post(
        self,
        request,
    ):
        """
        Reset a user's password.
        """

        serializer = self.serializer_class(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        reset_password(
            raw_token=serializer.validated_data["token"],
            new_password=serializer.validated_data["password"],
        )

        return Response(
            {
                "success": True,
                "message": (
                    "Password has been reset successfully."
                ),
            },
            status=status.HTTP_200_OK,
        )