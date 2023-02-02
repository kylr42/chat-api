from starlette import status

from app.pkg.models.base import BaseAPIException

__all__ = ["MessageDoesNotExist", "MessageDoesNotBelongToUser"]


class MessageDoesNotBelongToUser(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Message does not belong to user."


class MessageDoesNotExist(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Message does not exist."
