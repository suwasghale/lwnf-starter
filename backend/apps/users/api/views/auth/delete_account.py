"""
Views for deleting the authenticated user's account.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.api.serializers.auth import (
    DeleteAccountSerializer,
)

from apps.users.services.auth.delete_account import (
    delete_account,
)


class DeleteAccountAPIView(APIView):
    """
    Permanently deactivate the authenticated user's account.

    Security:
        - Authentication required.
        - Current password must be provided.
        - Revokes every active refresh token.
        - Invalidates every outstanding authentication token.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def delete(
        self,
        request,
    ) -> Response:
        serializer = DeleteAccountSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        delete_account(
            user=request.user,
            password=serializer.validated_data["password"],
        )

        return Response(
            {
                "detail": (
                    "Your account has been deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )