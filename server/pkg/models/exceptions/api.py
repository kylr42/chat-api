from server.pkg.models.base import BaseAPIException

__all__ = [
    "BadRequest",
    "UnexpectedError",
    "UnexpectedStatus",
]


class BadRequest(BaseAPIException):
    """Internal Server Error."""

    status_code = 400
    message = "Bad Request"


class UnexpectedError(BaseAPIException):
    """Internal Server Error."""

    status_code = 500
    message = "Unexpected Error"


class UnexpectedStatus(BaseAPIException):
    """Internal Server Error."""

    status_code = 500
    message = "Unexpected Status"
