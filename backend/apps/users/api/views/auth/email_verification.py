"""
Email verification API endpoint.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse
from core.api.schemas import (
    success_schema,
    bad_request_schema,
)

from apps.users.api.serializers.auth.email_verification import (
    EmailVerificationSerializer,
)

from apps.users.services.auth.email_verification import (
    verify_email,
)


@extend_schema(
    tags=["Authentication"],
    summary="Verify email address",
    description="Verify a user's email address using the verification token.",
    request=EmailVerificationSerializer,
    responses={
        200: success_schema(
            description="Email verified successfully.",
        ),
        400: bad_request_schema(),
    },
)
class EmailVerificationAPIView(BaseAPIView):
    """
    Verify a user's email.
    """

    authentication_classes = ()

    permission_classes = (
        AllowAny,
    )

    serializer_class = (
        EmailVerificationSerializer
    )

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        verify_email(
            raw_token=serializer.validated_data["token"],
        )

        return SuccessResponse.ok(
            message=(
                "Email address verified successfully."
            ),
        )