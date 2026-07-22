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

from apps.users.api.views.auth.login import (
    LoginAPIView,
)

from apps.users.api.views.auth.token_refresh import (
    TokenRefreshAPIView,   
)

from apps.users.api.views.auth.logout import (
    LogoutAPIView,
)

from apps.users.api.views.auth.logout_all import (
    LogoutAllAPIView,
)

from apps.users.api.views.auth.me import (
    CurrentUserAPIView,
)

from apps.users.api.views.auth.change_password import (
    ChangePasswordAPIView,
)

from apps.users.api.views.auth.forgot_password import (
    ForgotPasswordAPIView,
)

from apps.users.api.views.auth.reset_password import (
    ResetPasswordAPIView,
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
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        TokenRefreshAPIView.as_view(),
        name="token-refresh",
    ),
    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),
    path(
        "logout-all/",
        LogoutAllAPIView.as_view(),
        name="logout-all",
    ),
    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="me",
    ),
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset-reset",
    ),
]