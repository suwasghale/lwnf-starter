"""
Profile model.

Stores personal, contact, preference, and public profile information
that should not live inside the authentication User model.
"""

from __future__ import annotations

import uuid
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField


from apps.users.choices import GenderChoices
from apps.users.models.user import User


class Profile(models.Model):
    """
    Extended profile information for a user.

    Authentication-related fields belong to User.

    Personal, public, and preference-related fields belong here.
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
        help_text="Unique identifier for the profile.",
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User",
    )

    # ------------------------------------------------------------------
    # Personal Information
    # ------------------------------------------------------------------

    avatar = models.ImageField(
        upload_to="profiles/avatars/",
        blank=True,
        null=True,
        verbose_name="Avatar",
    )

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
        verbose_name="Gender",
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of birth",
    )
    
    nationality = CountryField(
            blank=True,
            null=True,
            verbose_name="Nationality",
    )

    # ------------------------------------------------------------------
    # Contact Information
    # ------------------------------------------------------------------

    phone_number = PhoneNumberField(
        blank=True,
        region="FR",
    )

    # ------------------------------------------------------------------
    # Public Information
    # ------------------------------------------------------------------

    biography = models.TextField(
        blank=True,
        verbose_name="Biography",
        help_text="Short public biography.",
    )

    # ------------------------------------------------------------------
    # Social Links
    # ------------------------------------------------------------------

    # facebook_url = models.URLField(
    #     blank=True,
    #     verbose_name="Facebook URL",
    # )

    # ------------------------------------------------------------------
    # Preferences
    # ------------------------------------------------------------------

    preferred_language = models.CharField(
        max_length=10,
        default="fr",
        verbose_name="Preferred language",
    )

    timezone = TimeZoneField(
        default="Europe/Paris",
        verbose_name="Timezone",
    )

    # ------------------------------------------------------------------
    # Audit Fields
    # ------------------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated at",
    )

    # ------------------------------------------------------------------
    # Computed Properties
    # ------------------------------------------------------------------

    @property
    def age(self) -> int | None:
        """
        Calculate user's age from date_of_birth.
        """
        if not self.date_of_birth:
            return None

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (
                    self.date_of_birth.month,
                    self.date_of_birth.day,
                )
            )
        )

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def clean(self) -> None:
        """
        Model-level validation.
        """

        super().clean()

        if (
            self.date_of_birth
            and self.date_of_birth > timezone.now().date()
        ):
            raise ValidationError(
                {
                    "date_of_birth": (
                        "Date of birth cannot be in the future."
                    )
                }
            )

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        """
        Run validation before saving.
        """

        self.full_clean()

        return super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # String Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"Profile: {self.user.email}"

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=["created_at"],
                name="profile_created_idx",
            ),
            models.Index(
                fields=["phone_number"],
                name="profile_phone_idx",
            ),
        ]