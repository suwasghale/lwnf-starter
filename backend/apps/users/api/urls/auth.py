"""
Authentication API endpoints.
"""

from __future__ import annotations

from django.urls import path

from apps.users.api.views.auth.registration import (
    RegistrationAPIView,
)
from apps.users.api.views.auth.password_reset import (
    PasswordResetConfirmAPIView,
    PasswordResetRequestAPIView,
    PasswordResetVerifyAPIView,
)

app_name = "auth"

urlpatterns = [
    path(
        "register/",
        RegistrationAPIView.as_view(),
        name="register",
    ),
    path(
        "password-reset/",
        PasswordResetRequestAPIView.as_view(),
        name="password-reset",
    ),
    path(
        "password-reset/verify/",
        PasswordResetVerifyAPIView.as_view(),
        name="password-reset-verify",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
]