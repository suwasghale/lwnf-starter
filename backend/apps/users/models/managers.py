"""
LWNF Backend

Custom User Manager

Responsibilities
----------------
- Create regular users.
- Create staff users.
- Create superusers.
- Normalize email addresses.
- Validate required authentication fields.

Business logic such as registration, email verification,
JWT generation, profile creation, etc. belongs inside
the services layer—not here.
"""

from __future__ import annotations

from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Authentication is based on email instead of username.
    """

    use_in_migrations = True

    # ---------------------------------------------------------
    # Internal creator
    # ---------------------------------------------------------

    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields: Any,
    ):
        """
        Internal helper used by every user creation method.

        This method should never be called directly outside
        of this manager.
        """

        if not email:
            raise ValueError("An email address is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)

        user.full_clean(exclude=["password"])

        user.save(using=self._db)

        return user

    # ---------------------------------------------------------
    # Regular User
    # ---------------------------------------------------------

    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create a normal authenticated user.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("date_joined", timezone.now())

        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )

    # ---------------------------------------------------------
    # Staff User
    # ---------------------------------------------------------

    def create_staff(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ):
        """
        Create an admin/staff account.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("date_joined", timezone.now())

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Staff user must have is_staff=True.")

        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )

    # ---------------------------------------------------------
    # Superuser
    # ---------------------------------------------------------

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ):
        """
        Create a Django superuser.
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("date_joined", timezone.now())

        required_flags = {
            "is_active": True,
            "is_staff": True,
            "is_superuser": True,
        }

        for field, expected in required_flags.items():
            if extra_fields.get(field) != expected:
                raise ValueError(
                    f"Superuser must have {field}={expected}."
                )

        return self._create_user(
            email=email,
            password=password,
            **extra_fields,
        )

"""

Features to improve later (not now):

Once the project grows, we should enhance with:

- A custom QuerySet (UserQuerySet) for methods like .active(), .verified(), .staff(), etc.
- Returning a custom UserQuerySet via get_queryset().
- Bulk creation helpers if needed.
- Additional database optimizations for large datasets.

"""