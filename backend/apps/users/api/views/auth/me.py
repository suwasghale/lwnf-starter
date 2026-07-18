"""
API endpoint for retrieving the authenticated user.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema

from rest_framework.request import Request
from rest_framework.response import Response

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse
from core.api.schemas import (
    success_schema,
    unauthorized_schema,
)

from apps.users.api.serializers.auth.me import (
    CurrentUserSerializer,
)

from apps.users.services.auth.me import (
    get_current_user,
)


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
class CurrentUserAPIView(BaseAPIView):
    """
    Retrieve the authenticated user.
    """

    serializer_class = CurrentUserSerializer

    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:

        user = get_current_user(
            user=request.user,
        )

        serializer = self.get_serializer(
            user,
        )

        return SuccessResponse.ok(
            message="Current user retrieved successfully.",
            data=serializer.data,
        )