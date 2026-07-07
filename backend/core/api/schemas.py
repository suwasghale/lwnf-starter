"""
Reusable OpenAPI schema helpers.

This module centralizes reusable drf-spectacular
schema definitions.

Views should import these helpers instead of
duplicating OpenApiResponse definitions.
"""

from drf_spectacular.utils import OpenApiResponse


def success_schema(
    description: str = "Request completed successfully.",
) -> OpenApiResponse:
    return OpenApiResponse(
        description=description,
    )


def created_schema(
    description: str = "Resource created successfully.",
) -> OpenApiResponse:
    return OpenApiResponse(
        description=description,
    )


def accepted_schema(
    description: str = "Request accepted.",
) -> OpenApiResponse:
    return OpenApiResponse(
        description=description,
    )


def no_content_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="No content.",
    )


def bad_request_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Validation error.",
    )


def unauthorized_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Authentication required.",
    )


def forbidden_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Permission denied.",
    )


def not_found_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Requested resource was not found.",
    )


def conflict_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Conflict.",
    )


def too_many_requests_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Too many requests.",
    )


def server_error_schema() -> OpenApiResponse:
    return OpenApiResponse(
        description="Internal server error.",
    )
