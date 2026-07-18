from __future__ import annotations

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request


class BaseAPIView(GenericAPIView):
    """
    Base API view for the entire project.
    """

    # authentication_classes = ()
    # permission_classes = ()
    # throttle_classes = ()

    serializer_class = None
    queryset = None

    def get_serializer_context(self) -> dict:
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    # ------------------------------------------------------------------
    # Client helpers
    # ------------------------------------------------------------------

    def get_client_ip(self) -> str | None:
        forwarded = self.request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            return forwarded.split(",")[0].strip()

        return self.request.META.get("REMOTE_ADDR")

    def get_user_agent(self) -> str:
        return self.request.headers.get(
            "User-Agent",
            "",
        )

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    @property
    def current_user(self):
        return self.request.user

    @property
    def is_authenticated(self) -> bool:
        return bool(
            self.request.user
            and self.request.user.is_authenticated
        )


class AuthenticatedAPIView(BaseAPIView):
    permission_classes = (
        IsAuthenticated,
    )