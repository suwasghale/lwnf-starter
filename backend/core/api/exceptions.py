"""
Global DRF exception handler.

Every exception raised by the application is converted into a
standardized JSON response.

Response format:

{
    "success": false,
    "message": "...",
    "errors": {...}
}
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.exceptions import LWNFException


def custom_exception_handler(exc, context):
    """
    Global DRF exception handler.
    """

    response = exception_handler(exc, context)

    # ============================================================
    # DRF Exceptions
    # ============================================================

    if response is not None:
        message = "Request failed."
        errors = None

        if isinstance(response.data, dict):

            if "detail" in response.data:
                message = str(response.data["detail"])

            else:
                errors = response.data

        else:
            errors = response.data

        response.data = {
            "success": False,
            "message": message,
            "errors": errors,
        }

        return response

    # ============================================================
    # Application Exceptions
    # ============================================================

    if isinstance(exc, LWNFException):

        return Response(
            {
                "success": False,
                "message": exc.message,
                "errors": None,
            },
            status=getattr(
                exc,
                "status_code",
                status.HTTP_400_BAD_REQUEST,
            ),
        )

    # ============================================================
    # Unexpected Exceptions
    # ============================================================
    
    # During development, let Django show the full traceback.
    raise exc

    # return Response(
    #     {
    #         "success": False,
    #         "message": (
    #             "An unexpected server error occurred."
    #         ),
    #         "errors": None,
    #     },
    #     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    # )
    
