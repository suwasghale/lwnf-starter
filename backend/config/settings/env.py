"""
Environment configuration.

Responsibilities:
- Define project paths.
- Load the active `.env` file exactly once.
- Expose the shared `env` object.
- Prevent every settings component from loading `.env` repeatedly.
"""

from pathlib import Path
import os
import environ

# ------------------------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------------------------

# backend/
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Alias used by Django settings
BASE_DIR = ROOT_DIR

# ------------------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------------------

env = environ.Env()

if "prod" in os.environ.get("DJANGO_SETTINGS_MODULE", ""):
    env.read_env(ROOT_DIR / ".env.production")
else:
    env.read_env(ROOT_DIR / ".env")