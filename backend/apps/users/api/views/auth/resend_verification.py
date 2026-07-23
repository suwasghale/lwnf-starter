"""
Views for resending email verification.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ) -> Response:
        serializer = ResendVerificationSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        resend_email_verification(
            user=request.user,
            created_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get(
                "HTTP_USER_AGENT",
                "",
            ),
        )

        return Response(
            {
                "detail": (
                    "A new verification email has been sent."
                )
            },
            status=status.HTTP_200_OK,
        )