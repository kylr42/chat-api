from pydantic.types import PositiveInt

from app.pkg.models.user import UserFields
from app.pkg.models.base import BaseModel
from app.pkg.models.types import EncryptedSecretBytes

__all__ = [
    "UserProfile",
    "ReadUserByIdQuery",
    "CreateUserProfileCommand",
    "UpdateUserProfileCommand",
    "ChangeUserPasswordCommand",
]


class BaseUserProfile(BaseModel):
    """Base model for user profile."""


class UserProfile(BaseUserProfile):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    phone_number: str = UserFields.phone_number


class CreateUserProfileCommand(BaseUserProfile):
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    phone_number: str = UserFields.phone_number


class UpdateUserProfileCommand(BaseUserProfile):
    username: str = UserFields.username
    phone_number: str = UserFields.phone_number


class ChangeUserPasswordCommand(BaseUserProfile):
    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: EncryptedSecretBytes = UserFields.new_password


# Query
class ReadUserByIdQuery(BaseUserProfile):
    id: PositiveInt = UserFields.id
