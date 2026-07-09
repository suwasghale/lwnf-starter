"""
Authentication API endpoints.
"""

from __future__ import annotations

from django.urls import path

from apps.users.api.views.auth.registration import (
    RegistrationAPIView,
)

from apps.users.api.views.auth.email_verification import (
    EmailVerificationAPIView,
)


app_name = "auth"

urlpatterns = [
    path(
        "register/",
        RegistrationAPIView.as_view(),
        name="register",
    ),
    path(
        "verify-email/",
        EmailVerificationAPIView.as_view(),
        name="verify-email",
    ),
]