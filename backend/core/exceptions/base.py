"""
Base exceptions for the LWNF project.
"""


class LWNFException(Exception):
    """
    Base exception for the LWNF project.

    Every custom application exception should inherit from this class.
    """

    default_message = "An unexpected application error occurred."
    status_code = 400
    
    def __init__(
        self,
        message: str | None = None,
    ):
        self.message = message or self.default_message
        super().__init__(self.message)