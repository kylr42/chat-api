from pydantic.fields import Field
from pydantic.types import PositiveInt, SecretStr

from server.pkg.models.base import BaseModel

__all__ = [
    "User",
    "UserFields",
    "ReadUserByIdQuery",
    "ReadUserByUserNameQuery",
    "ReadUserProfileQuery",
]


class UserFields:
    id = Field(description="User id.", example=2)
    username = Field(description="User Login", example="TestTest")
    phone_number = Field(
        description="User phone number.",
        example="+380501234567",
        min_length=9,
        max_length=15,
        regex=r"^\+?1?\d{9,15}$",
    )
    is_active = Field(description="User is active.", example=True, default=False)
    access_token = Field(
        description="User access token.",
        example="example.access.token",
    )


class BaseUser(BaseModel):
    """Base model for user."""


class User(BaseUser):
    id: PositiveInt = UserFields.id
    username: str = UserFields.username
    phone_number: str = UserFields.phone_number
    is_active: bool = UserFields.is_active


# Query
class ReadUserByUserNameQuery(BaseUser):
    username: str = UserFields.username
    access_token: SecretStr = UserFields.access_token


class ReadUserByIdQuery(BaseUser):
    id: PositiveInt = UserFields.id
    access_token: SecretStr = UserFields.access_token


class ReadUserProfileQuery(BaseUser):
    access_token: SecretStr = UserFields.access_token
