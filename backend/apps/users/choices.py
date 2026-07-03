"""
===============================================================================
LWNF Backend - User Choices
===============================================================================

Centralized reusable enumerations for the Users application.

Example
-------
status = models.CharField(
    max_length=20,
    choices=AccountStatusChoices.choices,
    default=AccountStatusChoices.ACTIVE,
)

===============================================================================
"""

from django.db import models


# =============================================================================
# Gender
# =============================================================================


class GenderChoices(models.TextChoices):
    """Supported gender identities."""

    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"


# =============================================================================
# Preferred Language
# =============================================================================


class LanguageChoices(models.TextChoices):
    """Supported interface languages."""

    ENGLISH = "en", "English"
    FRENCH = "fr", "French"

# =============================================================================
# Account Status
# =============================================================================


class AccountStatusChoices(models.TextChoices):
    """
    Lifecycle state of a user account.

    ACTIVE
        Fully usable account.

    INACTIVE
        Disabled manually or by administrator.

    PENDING
        Registered but awaiting verification.

    SUSPENDED
        Temporarily blocked.

    ARCHIVED
        Historical record only.
    """

    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    SUSPENDED = "suspended", "Suspended"
    ARCHIVED = "archived", "Archived"


# =============================================================================
# User Type
# =============================================================================


class UserTypeChoices(models.TextChoices):
    """
    High-level user classification.

    This is NOT a permission system.

    Authorization should use:
        - Django Groups
        - Django Permissions

    User type is primarily used for business logic.
    """

    ADMIN = "admin", "Administrator"
    MEMBER = "member", "Member"
    SPONSOR = "sponsor", "Sponsor"
    VOLUNTEER = "volunteer", "Volunteer"

# =============================================================================
# Address Type
# =============================================================================

class AddressTypeChoices(models.TextChoices):
    """Address categories."""

    HOME = "home", "Home"
    WORK = "work", "Work"
    BILLING = "billing", "Billing"
    SHIPPING = "shipping", "Shipping"
    OTHER = "other", "Other"

# =============================================================================
# Notification Channel
# =============================================================================


class NotificationChannelChoices(models.TextChoices):
    """Preferred notification delivery channel."""

    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    PUSH = "push", "Push Notification"


# =============================================================================
# File Visibility
# =============================================================================


class VisibilityChoices(models.TextChoices):
    """Visibility level for uploaded content."""

    PRIVATE = "private", "Private"
    INTERNAL = "internal", "Internal"
    PUBLIC = "public", "Public"