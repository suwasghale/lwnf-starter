"""
Reusable API response helpers.

Every successful API response in the project should be
generated through these helpers to keep a consistent
response structure.

Response format:
SUCCESSFUL RESPONSE: 
{
    "success": true,
    "message": "...",
    "data": {...}
}

ERROR RESPONSE:
{
    "success": false,
    "message": "Invalid token.",
    "errors": {
        "token": [
            "Token has expired."
        ]
    }
}

"""

from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response


# =============================================================================
# Internal
# =============================================================================


def _response(
    *,
    success: bool,
    message: str,
    data: Any = None,
    status_code: int,
    headers: dict[str, str] | None = None,
) -> Response:
    """
    Build a standardized API response.
    """

    payload = {
        "success": success,
        "message": message,
        "data": data,
    }

    return Response(
        payload,
        status=status_code,
        headers=headers,
    )


# =============================================================================
# Success Responses
# =============================================================================


def success_response(
    *,
    message: str = "Success.",
    data: Any = None,
) -> Response:
    """
    HTTP 200
    """

    return _response(
        success=True,
        message=message,
        data=data,
        status_code=status.HTTP_200_OK,
    )


def created_response(
    *,
    message: str = "Resource created.",
    data: Any = None,
    headers: dict[str, str] | None = None,
) -> Response:
    """
    HTTP 201
    """

    return _response(
        success=True,
        message=message,
        data=data,
        status_code=status.HTTP_201_CREATED,
        headers=headers,
    )


def accepted_response(
    *,
    message: str = "Request accepted.",
    data: Any = None,
) -> Response:
    """
    HTTP 202
    """

    return _response(
        success=True,
        message=message,
        data=data,
        status_code=status.HTTP_202_ACCEPTED,
    )


def no_content_response() -> Response:
    """
    HTTP 204

    RFC 9110 states that 204 responses MUST NOT
    contain a response body.
    """

    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )