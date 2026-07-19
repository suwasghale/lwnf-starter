"""
API endpoint for changing the authenticated user's password.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse
from core.api.schemas import (
    success_schema,
    bad_request_schema,
    unauthorized_schema,
    too_many_requests_schema,
)

from core.api.throttles import PasswordChangeThrottle

from apps.users.api.serializers.auth.change_password import (
    ChangePasswordSerializer,
)

from apps.users.services.auth.change_password import (
    change_password,
)


@extend_schema(
    tags=["Authentication"],
    summary="Change password",
    description=(
        "Change the password of the currently authenticated user."
    ),
    request=ChangePasswordSerializer,
    responses={
        200: success_schema(
            description="Password changed successfully.",
        ),
        400: bad_request_schema(),
        401: unauthorized_schema(),
        429: too_many_requests_schema(),
    },
)
class ChangePasswordAPIView(BaseAPIView):
    """
    Change the authenticated user's password.
    """
    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = ChangePasswordSerializer

    throttle_classes = (
        PasswordChangeThrottle,
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

        change_password(
            user=request.user,
            current_password=serializer.validated_data[
                "current_password"
            ],
            new_password=serializer.validated_data[
                "new_password"
            ],
        )

        return SuccessResponse.ok(
            message="Password changed successfully.",
        )