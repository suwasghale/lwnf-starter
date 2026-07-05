"""
Base API views shared across the project.

These classes provide common functionality for every API endpoint.

Responsibilities:

- client IP extraction
- user agent extraction
- convenience response helpers
- common request utilities

Business logic NEVER belongs here.
"""

from __future__ import annotations

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated


class BaseAPIView(APIView):
    """
    Base class for all project API views.

    Every API view should inherit from this class instead
    of DRF's APIView directly.
    """

    permission_classes = (
        permissions.AllowAny,
    )

    # ============================================================
    # Client Information
    # ============================================================

    @staticmethod
    def get_client_ip(
        request: Request,
    ) -> str | None:
        """
        Return the client's real IP address.

        Supports reverse proxies using X-Forwarded-For.
        """

        forwarded_for = request.META.get(
            "HTTP_X_FORWARDED_FOR",
        )

        if forwarded_for:
            return (
                forwarded_for
                .split(",")[0]
                .strip()
            )

        return request.META.get(
            "REMOTE_ADDR",
        )

    @staticmethod
    def get_user_agent(
        request: Request,
    ) -> str:
        """
        Return the client's user agent.
        """

        return request.headers.get(
            "User-Agent",
            "",
        )

    # ============================================================
    # Convenience Properties
    # ============================================================

    @property
    def current_user(self):
        """
        Return the authenticated user.
        """

        return self.request.user

    @property
    def is_authenticated(self) -> bool:
        """
        Whether the current request is authenticated.
        """

        return bool(
            self.request.user
            and self.request.user.is_authenticated
        )
        

"""
Reusable base API views.

These classes provide shared behavior for every API endpoint.

Business logic should never live here.
"""


class BaseAPIView(GenericAPIView):
    """
    Base API view for the project.

    Features:

    - serializer support
    - queryset support
    - DRF GenericAPIView utilities
    """

    authentication_classes = ()

    permission_classes = ()

    throttle_classes = ()

    serializer_class = None

    queryset = None

    def get_serializer_context(self) -> dict:
        """
        Extend serializer context.
        """

        context = super().get_serializer_context()

        context.update(
            {
                "request": self.request,
            }
        )

        return context


class AuthenticatedAPIView(BaseAPIView):
    """
    Base class for authenticated endpoints.
    """

    permission_classes = (
        IsAuthenticated,
    )