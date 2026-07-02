""" 

User
│
├── UUID primary key
├── Email login
├── First name
├── Last name
├── Active
├── Staff
├── Superuser
├── Verified
├── Last login
├── Last seen
├── Date joined
├── Created at
├── Updated at
│
├── UserManager
│
├── Properties
│     ├── full_name
│     ├── short_name
│
├── Methods
│     ├── clean()
│     ├── save()
│     ├── email_user()
│     ├── __str__()
│
├── Meta
│     ├── ordering
│     ├── indexes
│     ├── constraints
│     ├── verbose names
│
└── Type hints

Authentication
--------------
id
email
password

Personal
--------
first_name
last_name

Authorization
-------------
is_active
is_staff
is_superuser
is_verified

Tracking
--------
last_login
last_seen
date_joined
created_at
updated_at

Imports: 
Standard Library

↓

Django

↓

Third Party

↓

Local Project

apps/users/models/user.py

──────────────────────────────

1. Module docstring               ⭐

2. Imports                        ⭐

3. User class definition          ⭐

4. Identity fields

5. Authentication fields

6. Personal fields

7. Permission fields

8. Activity fields

9. Timestamp fields

10. Django auth configuration

11. Properties

12. Instance methods

13. Meta

14. End of file review

"""

"""
LWNF Backend

Custom User Model

This module defines the project's primary authentication model.

Authentication Strategy
-----------------------
- UUID primary key
- Email-based authentication
- Custom UserManager
- No username field

Responsibilities
----------------
- Store authentication credentials.
- Store essential identity information.
- Manage permissions and account status.
- Provide helper properties and instance methods.

Non-Responsibilities
--------------------
The following belong to other models or services:

- User profile
- Addresses
- Avatar
- Social accounts
- Email verification workflow
- Registration business logic
- Authentication services
- JWT generation
- Password reset workflow

Related Modules
---------------
- models.managers
- models.profile
- models.address
- services.authentication
- services.registration
"""

from __future__ import annotations

import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom authentication model.

    Email is used as the unique login identifier instead of username.

    This model intentionally contains only authentication and identity
    information. Additional user-related data belongs in dedicated models
    such as Profile and Address.
    """
    
        # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
        help_text=_("Unique identifier for the user."),
    )

    # -------------------------------------------------------------------------
    # Authentication
    # -------------------------------------------------------------------------

    email = models.EmailField(
        unique=True,
        max_length=254,
        db_index=True,
        verbose_name=_("Email address"),
        help_text=_("Unique email address used for authentication."),
    )

    # -------------------------------------------------------------------------
    # Personal Information
    # -------------------------------------------------------------------------

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("First name"),
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_("Last name"),
    )

    # -------------------------------------------------------------------------
    # Account Status
    # -------------------------------------------------------------------------

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_(
            "Designates whether this account is active."
        ),
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Staff status"),
        help_text=_(
            "Designates whether the user can access the admin site."
        ),
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("Verified"),
        help_text=_(
            "Indicates whether the user's email address has been verified."
        ),
    )

    # -------------------------------------------------------------------------
    # Activity
    # -------------------------------------------------------------------------

    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Last seen"),
    )

    # -------------------------------------------------------------------------
    # Timestamps
    # -------------------------------------------------------------------------
    
    # Business meaning:"When did this person join LWNF?"
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date joined"),
    )

    # Database record creation timestamp.
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    
    # -------------------------------------------------------------------------
    # Authentication Configuration
    # -------------------------------------------------------------------------

    objects = UserManager()

    EMAIL_FIELD = "email"

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS: list[str] = []
    
    # -------------------------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        """
        Return the user's full name.

        Returns:
            str: First name and last name combined, with extra whitespace removed.
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def short_name(self) -> str:
        """
        Return the preferred short display name.

        Priority:
            1. First name
            2. Email address
        """
        return self.first_name or self.email

    # -------------------------------------------------------------------------
    # Instance Methods
    # -------------------------------------------------------------------------

    def clean(self) -> None:
        """
        Normalize and validate model data before saving.

        This method is automatically called by `full_clean()`.
        """

        super().clean()

        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)

    def save(self, *args, **kwargs) -> None:
        """
        Save the user instance.

        Always perform model validation before persisting
        the object to the database.
        """

        self.full_clean()

        super().save(*args, **kwargs)

    def email_user(
        self,
        subject: str,
        message: str,
        from_email: str | None = None,
        **kwargs,
    ) -> None:
        """
        Send an email to this user.

        This mirrors Django's default User implementation,
        making the model compatible with Django's ecosystem.
        """

        from django.core.mail import send_mail

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[self.email],
            **kwargs,
        )

    def __str__(self) -> str:
        """
        Human-readable representation.
        """

        return self.full_name or self.email