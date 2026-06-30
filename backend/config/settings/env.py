"""
Environment configuration.

Responsibilities:
- Define project paths.
- Load the active `.env` file exactly once.
- Expose the shared `env` object.
- Prevent every settings component from loading `.env` repeatedly.
"""

from pathlib import Path

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

# Load active environment file
ENV_FILE = ROOT_DIR / ".env"

if ENV_FILE.exists():
    environ.Env.read_env(ENV_FILE)