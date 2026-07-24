"""
API endpoint for managing the authenticated user's avatar.
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

from apps.users.api.serializers.profile.avatar import (
    AvatarUploadSerializer,
)

from apps.users.api.serializers.auth.me import (
    CurrentUserSerializer,
)

from apps.users.services.account.update_avatar import (
    update_avatar,
)

from apps.users.selectors.user import (
    get_user_with_profile,
)


@extend_schema(
    tags=["Account"],
    summary="Update avatar",
    description="Upload or replace the authenticated user's avatar.",
    request=AvatarUploadSerializer,
    responses={
        200: success_schema(
            description="Avatar updated successfully.",
            response=CurrentUserSerializer,
        ),
        400: bad_request_schema(),
        401: unauthorized_schema(),
    },
)
class AvatarAPIView(BaseAPIView):
    """
    Upload or replace the authenticated user's avatar.
    """

    serializer_class = AvatarUploadSerializer

    def patch(
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

        user = update_avatar(
            user=request.user,
            avatar=serializer.validated_data["avatar"],
        )

        user = get_user_with_profile(
            user_id=user.id,
        )

        response_data = CurrentUserSerializer(
            user,
        ).data

        return SuccessResponse.ok(
            message="Avatar updated successfully.",
            data=response_data,
        )