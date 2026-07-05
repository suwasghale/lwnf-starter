"""
Reusable OpenAPI schema helpers.

This module centralizes reusable drf-spectacular
schema definitions.

Views should import these helpers instead of
duplicating OpenApiResponse definitions.
"""

from __future__ import annotations

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
)


# =============================================================================
# Common Responses
# =============================================================================


SUCCESS_RESPONSE = OpenApiResponse(
    description="Request completed successfully.",
)


CREATED_RESPONSE = OpenApiResponse(
    description="Resource created successfully.",
)


ACCEPTED_RESPONSE = OpenApiResponse(
    description="Request accepted.",
)


NO_CONTENT_RESPONSE = OpenApiResponse(
    description="No content.",
)


BAD_REQUEST_RESPONSE = OpenApiResponse(
    description="Validation error.",
)


UNAUTHORIZED_RESPONSE = OpenApiResponse(
    description="Authentication required.",
)


FORBIDDEN_RESPONSE = OpenApiResponse(
    description="Permission denied.",
)


NOT_FOUND_RESPONSE = OpenApiResponse(
    description="Requested resource was not found.",
)


CONFLICT_RESPONSE = OpenApiResponse(
    description="Conflict.",
)


TOO_MANY_REQUESTS_RESPONSE = OpenApiResponse(
    description="Too many requests.",
)


SERVER_ERROR_RESPONSE = OpenApiResponse(
    description="Internal server error.",
)


# =============================================================================
# Common Examples
# =============================================================================


SUCCESS_EXAMPLE = OpenApiExample(
    name="Success",
    value={
        "success": True,
        "message": "Operation completed successfully.",
        "data": {},
    },
    response_only=True,
)


VALIDATION_ERROR_EXAMPLE = OpenApiExample(
    name="Validation Error",
    value={
        "success": False,
        "message": "Validation failed.",
        "errors": {
            "email": [
                "This field is required."
            ]
        },
    },
    response_only=True,
)


INVALID_TOKEN_EXAMPLE = OpenApiExample(
    name="Invalid Token",
    value={
        "success": False,
        "message": "Password reset token is invalid or has expired.",
    },
    response_only=True,
)


RATE_LIMIT_EXAMPLE = OpenApiExample(
    name="Rate Limited",
    value={
        "success": False,
        "message": "Request was throttled.",
    },
    response_only=True,
)