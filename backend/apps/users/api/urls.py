"""
Users API URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "users"

urlpatterns = [
    path(
        "auth/",
        include(
            (
                "apps.users.api.urls.auth",
                "auth",
            ),
        ),
    ),
]