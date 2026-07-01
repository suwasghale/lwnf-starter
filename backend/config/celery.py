"""
===============================================================================
LWNF Celery Application
===============================================================================

Creates and configures the Celery application for the project.

Responsibilities:
- Initialize Celery
- Load Django settings
- Auto-discover tasks
===============================================================================
"""

import os

from celery import Celery

# Default Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.dev",
)

# Create Celery application
app = Celery("lwnf")

# Load configuration from Django settings
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# Automatically discover tasks.py inside installed apps
app.autodiscover_tasks()