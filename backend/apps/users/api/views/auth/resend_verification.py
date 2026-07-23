"""
Views for resending email verification.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers.auth import (
    ResendVerificationSerializer,
)

from apps.users.services.auth.email_verification import (
    resend_email_verification,
)


class ResendVerificationAPIView(APIView):
    """
    Resend an email verification link.

    Requires authentication.
    """
    authentication_classes = []
    permission_classes = [
        AllowAny,
    ]

    def post(
        self,
        request,
    ) -> Response:
        print("1")
        serializer = ResendVerificationSerializer(
            data=request.data,
        )
        print("2")
        serializer.is_valid(
            raise_exception=True,
        )
        print("3")
        print(serializer.validated_data)
        print("calling service")
        resend_email_verification(
            email=serializer.validated_data["email"],
            created_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get(
                "HTTP_USER_AGENT",
                "",
            ),
        )
        print("service finished")

        return Response(
            {
                "detail": (
                    "If the account exists and is not yet verified, a verification email has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )