from drf_spectacular.utils import extend_schema

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse

from apps.users.api.serializers.auth.token_refresh import (
    TokenRefreshSerializer,
    TokenRefreshResponseSerializer,
)

from apps.users.services.auth.refresh import (
    refresh_access_token,
)


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
    request=TokenRefreshSerializer,
    responses={
        200: TokenRefreshResponseSerializer,
    },
)
class TokenRefreshAPIView(BaseAPIView):

    authentication_classes = ()

    permission_classes = (
        AllowAny,
    )

    serializer_class = TokenRefreshSerializer

    def post(self, request) -> Response:

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = refresh_access_token(
            refresh=serializer.validated_data["refresh"],
        )

        return SuccessResponse.ok(
            message="Access token refreshed.",
            data=data,
        )