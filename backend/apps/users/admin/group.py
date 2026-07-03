"""
Admin configuration for Django's built-in Group model.
"""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.db.models import Count, QuerySet


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    """
    Customized admin interface for Group.
    """

    # ---------------------------------------------------------
    # List View
    # ---------------------------------------------------------

    list_display = (
        "name",
        "user_count",
        "permission_count",
    )

    ordering = (
        "name",
    )

    list_per_page = 25

    # ---------------------------------------------------------
    # Searching
    # ---------------------------------------------------------

    search_fields = (
        "name",
    )

    # ---------------------------------------------------------
    # Auto Complete
    # ---------------------------------------------------------

    autocomplete_fields = (
        "permissions",
    )

    # ---------------------------------------------------------
    # Readonly Fields
    # ---------------------------------------------------------

    readonly_fields = (
        "user_count",
        "permission_count",
    )

    # ---------------------------------------------------------
    # Fieldsets
    # ---------------------------------------------------------

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "permissions",
                ),
            },
        ),
        (
            "Statistics",
            {
                "classes": ("collapse",),
                "fields": (
                    "user_count",
                    "permission_count",
                ),
            },
        ),
    )

    # ---------------------------------------------------------
    # Performance
    # ---------------------------------------------------------

    def get_queryset(self, request) -> QuerySet:
        """
        Optimize queryset.
        """
        queryset = super().get_queryset(request)

        return queryset.prefetch_related(
            "permissions",
            "user_set",
        ).annotate(
            total_users=Count("user", distinct=True),
            total_permissions=Count("permissions", distinct=True),
        )

    # ---------------------------------------------------------
    # Computed Fields
    # ---------------------------------------------------------

    @admin.display(description="Users")
    def user_count(self, obj: Group) -> int:
        """
        Return the number of users in this group.
        """
        return getattr(obj, "total_users", obj.user_set.count())

    @admin.display(description="Permissions")
    def permission_count(self, obj: Group) -> int:
        """
        Return the number of permissions assigned to this group.
        """
        return getattr(
            obj,
            "total_permissions",
            obj.permissions.count(),
        )