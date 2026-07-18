from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.base import BaseAPIView
from core.api.responses import SuccessResponse

from apps.users.api.serializers.auth.logout import (
    LogoutSerializer,
)

from apps.users.services.auth.logout import (
    logout,
)


@extend_schema(
    tags=["Authentication"],
    summary="Logout",
    request=LogoutSerializer,
)
class LogoutAPIView(BaseAPIView):

    permission_classes = (
        IsAuthenticated,
    )

    serializer_class = LogoutSerializer

    def post(self, request) -> Response:

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        logout(
            refresh=serializer.validated_data["refresh"],
        )

        return SuccessResponse.ok(
            message="Logout successful.",
        )