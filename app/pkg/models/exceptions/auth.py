from app.pkg.models.base import BaseAPIException

__all__ = [
    "IncorrectLengthFingerprint",
    "IncorrectUsernameOrPassword",
    "UserIsNotActive",
    "MethodNotAllowed",
    "PermissionDenied",
]


class IncorrectLengthFingerprint(BaseAPIException):
    status_code = 400
    message = "Incorrect fingerprint"


class IncorrectUsernameOrPassword(BaseAPIException):
    status_code = 406
    message = "Incorrect username or password or secret key"


class UserIsNotActive(BaseAPIException):
    status_code = 406
    message = "User is not active"


class MethodNotAllowed(BaseAPIException):
    status_code = 405
    message = "Method not allowed"


class PermissionDenied(BaseAPIException):
    status_code = 403
    message = "You don't have permission for this action"
