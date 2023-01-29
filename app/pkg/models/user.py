from pydantic.fields import Field
from pydantic.types import PositiveInt

from app.pkg.models.base import BaseModel
from app.pkg.models.types import EncryptedSecretBytes

__all__ = [
    "User",
    "UserFields",
    "CreateUserCommand",
    "ReadUserByIdQuery",
    "ReadUserByUserNameQuery",
    "UpdateUserCommand",
    "DeleteUserCommand",
    "ChangeUserPasswordCommand",
]


class UserFields:
    id = Field(description="User id.", example=2)
    username = Field(description="User Login", example="TestTest")
    password = Field(
        description="User password",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    old_password = Field(
        description="Old user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    new_password = Field(
        description="New user password.",
        example="strong password",
        min_length=6,
        max_length=256,
    )
    phone_number = Field(
        description="User phone number.",
        example="+380501234567",
        min_length=9,
        max_length=15,
        regex=r"^\+?1?\d{9,15}$",
    )
    is_active = Field(description="User is active.", example=True, is_active=True)


class BaseUser(BaseModel):
    """Base model for user."""


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    phone_number: str = UserFields.phone_number
    is_active: bool = UserFields.is_active


# Commands.
class CreateUserCommand(BaseUser):
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    phone_number: str = UserFields.phone_number
    is_active: bool = UserFields.is_active


class UpdateUserCommand(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    password: EncryptedSecretBytes = UserFields.password
    phone_number: str = UserFields.phone_number


class UpdateStatusUserCommand(BaseUser):
    id: PositiveInt = UserFields.id
    is_active: bool = UserFields.is_active


class DeleteUserCommand(BaseUser):
    id: PositiveInt = UserFields.id


class ChangeUserPasswordCommand(BaseUser):
    id: PositiveInt = UserFields.id
    old_password: EncryptedSecretBytes = UserFields.old_password
    new_password: EncryptedSecretBytes = UserFields.new_password


# Query
class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id
