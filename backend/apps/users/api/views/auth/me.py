"""
API endpoint for the authenticated user.

Supports:

- Retrieve current user
- Update current user's account/profile
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.request import Request
from rest_framework.response import Response

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse
from core.api.schemas import (
    success_schema,
    bad_request_schema,
    unauthorized_schema,
)

from apps.users.api.serializers.auth import (
    CurrentUserSerializer,
    UpdateProfileSerializer,
)

from apps.users.services.auth.me import (
    get_current_user,
)

from apps.users.services.account.update_profile import (
    update_profile,
)


class MeAPIView(BaseAPIView):
    """
    Retrieve and update the authenticated user.
    """

    serializer_class = CurrentUserSerializer

    # =========================================================================
    # GET
    # =========================================================================

    @extend_schema(
        tags=["Authentication"],
        summary="Current authenticated user",
        description="Retrieve the currently authenticated user.",
        responses={
            200: success_schema(
                description="Current user retrieved successfully.",
                response=CurrentUserSerializer,
            ),
            401: unauthorized_schema(),
        },
    )
    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Retrieve the authenticated user.
        """

        user = get_current_user(
            user=request.user,
        )

        return SuccessResponse.ok(
            message="Current user retrieved successfully.",
            data=self.get_serializer(user).data,
        )

    # =========================================================================
    # PATCH
    # =========================================================================

    @extend_schema(
        tags=["Authentication"],
        summary="Update current user profile",
        description=(
            "Partially update the authenticated user's "
            "account and profile."
        ),
        request=UpdateProfileSerializer,
        responses={
            200: success_schema(
                description="Profile updated successfully.",
                response=CurrentUserSerializer,
            ),
            400: bad_request_schema(),
            401: unauthorized_schema(),
        },
    )
    def patch(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Partially update the authenticated user's profile.
        """

        serializer = UpdateProfileSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = update_profile(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return SuccessResponse.ok(
            message="Profile updated successfully.",
            data=self.get_serializer(user).data,
        )