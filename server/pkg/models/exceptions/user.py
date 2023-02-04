from server.pkg.models.base import BaseAPIException

__all__ = ["UserNotFound"]


class UserNotFound(BaseAPIException):
    status_code = 404
    message = "User not found"
