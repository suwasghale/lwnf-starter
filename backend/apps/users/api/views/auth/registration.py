"""
API endpoint for user registration.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.api.serializers.auth.registration import (
    RegistrationSerializer,
)
from apps.users.services.auth.registration import (
    register_user,
)

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse
from core.api.schemas import (
    bad_request_schema,
    created_schema,
)
from core.api.throttles import RegistrationThrottle


@extend_schema(
    tags=["Authentication"],
    summary="Register a new user",
    description=(
        "Creates a new account and sends an email verification link."
    ),
    request=RegistrationSerializer,
    responses={
        201: created_schema(
            "Registration successful. "
            "Please verify your email address."
        ),
        400: bad_request_schema(),
    },
)
class RegistrationAPIView(BaseAPIView):
    """
    Register a new user.
    """

    authentication_classes = ()

    permission_classes = (
        AllowAny,
    )

    throttle_classes = (
        RegistrationThrottle,
    )

    serializer_class = RegistrationSerializer

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    )-> Response:
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        data = serializer.validated_data

        register_user(
            data=data,
            created_ip=self.get_client_ip(),
            user_agent=self.get_user_agent(),
        )

        return SuccessResponse.created(
            message=(
                "Registration successful. "
                "Please verify your email address."
            ),
        )