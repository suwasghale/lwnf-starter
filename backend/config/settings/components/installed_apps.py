"""
Installed applications configuration.

Split applications into:
- Django applications
- Third-party applications
- Local applications
"""

# ------------------------------------------------------------------------------
# Django Apps
# ------------------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ------------------------------------------------------------------------------
# Third-party Apps
# ------------------------------------------------------------------------------

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
]

# ------------------------------------------------------------------------------
# Local Apps
# ------------------------------------------------------------------------------

LOCAL_APPS = [
    "apps.users",
]

# ------------------------------------------------------------------------------
# Final Installed Apps
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    *DJANGO_APPS,
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]