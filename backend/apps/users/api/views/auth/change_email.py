"""
Views for changing a user's email address.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers.auth import (
    ConfirmEmailChangeSerializer,
    RequestEmailChangeSerializer,
)

from apps.users.services.auth.change_email import (
    confirm_email_change,
    request_email_change,
)


class RequestEmailChangeAPIView(APIView):
    """
    Request an email address change.

    Requires an authenticated user.

    Workflow:
        - Validate the requested email address.
        - Create an email change request.
        - Send a verification email to the new address.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def post(
        self,
        request,
    ) -> Response:
        serializer = RequestEmailChangeSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        request_email_change(
            user=request.user,
            new_email=serializer.validated_data["new_email"],
            created_ip=request.META.get("REMOTE_ADDR"),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )

        return Response(
            {
                "detail": (
                    "A verification email has been sent to your "
                    "new email address."
                )
            },
            status=status.HTTP_200_OK,
        )


class ConfirmEmailChangeAPIView(APIView):
    """
    Confirm an email address change.

    This endpoint is accessed through the verification
    link sent to the user's new email address.
    """

    authentication_classes = []

    permission_classes = []

    def post(
        self,
        request,
    ) -> Response:
        serializer = ConfirmEmailChangeSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        confirm_email_change(
            raw_token=serializer.validated_data["token"],
        )

        return Response(
            {
                "detail": (
                    "Your email address has been updated successfully."
                )
            },
            status=status.HTTP_200_OK,
        )