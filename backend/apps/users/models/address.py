"""
Address model.

Stores one or more addresses associated with a user.
"""

from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField


from apps.users.choices import AddressTypeChoices
from apps.users.models.user import User


class Address(models.Model):
    """
    Represents a postal address belonging to a user.
    """

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )

    # ------------------------------------------------------------------
    # Relationship
    # ------------------------------------------------------------------

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="User",
    )

    # ------------------------------------------------------------------
    # Address Information
    # ------------------------------------------------------------------

    address_type = models.CharField(
        max_length=20,
        choices=AddressTypeChoices.choices,
        default=AddressTypeChoices.HOME,
        verbose_name="Address type",
    )

    label = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Label",
        help_text="Optional custom label such as Parents' Home.",
    )

    street_address = models.CharField(
        max_length=255,
        verbose_name="Street address",
    )

    address_line_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Address line 2",
    )

    city = models.CharField(
        max_length=100,
        verbose_name="City",
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="State / Province",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Postal code",
    )

    country = CountryField(
        verbose_name="Country",
    )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    is_default = models.BooleanField(
        default=False,
        verbose_name="Default address",
    )

    # ------------------------------------------------------------------
    # Audit
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
    # Validation
    # ------------------------------------------------------------------

    def clean(self):
        """
        Ensure only one default address exists per user.
        """
        super().clean()

        if self.is_default:
            queryset = Address.objects.filter(
                user=self.user,
                is_default=True,
            )

            if self.pk:
                queryset = queryset.exclude(pk=self.pk)

            if queryset.exists():
                raise ValidationError(
                    {
                        "is_default": (
                            "A user can only have one default address."
                        )
                    }
                )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # String Representation
    # ------------------------------------------------------------------

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.get_address_type_display()}"
        )

    # ------------------------------------------------------------------
    # Meta
    # ------------------------------------------------------------------

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

        ordering = ("-is_default", "-created_at")

        indexes = [
            models.Index(
                fields=["user"],
                name="address_user_idx",
            ),
            models.Index(
                fields=["country"],
                name="address_country_idx",
            ),
            models.Index(
                fields=["city"],
                name="address_city_idx",
            ),
            models.Index(
                fields=["is_default"],
                name="address_default_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "address_type"],
                condition=models.Q(is_default=True),
                name="unique_default_address_per_type",
            )
        ]