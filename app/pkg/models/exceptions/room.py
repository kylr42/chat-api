from fastapi import status

from app.pkg.models.base import BaseAPIException

__all__ = ["RoomAlreadyExist", "RoomDoesNotExist"]


class RoomDoesNotExist(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Room does not exist."


class RoomAlreadyExist(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = "Room already exist."
