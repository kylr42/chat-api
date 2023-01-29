"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr

from app.pkg.models.types import EncryptedSecretBytes

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev`.
    """

    #: str: Name of API service
    API_INSTANCE_APP_NAME: str

    #: str: Default username.
    API_DEFAULT_USERNAME: str
    #: EncryptedSecretBytes: Default user password.
    API_DEFAULT_PASSWORD: EncryptedSecretBytes
    #: str: Default user phone number.
    API_DEFAULT_PHONE_NUMBER: str

    #: str: Postgresql host.
    POSTGRES_HOST: str
    #: PositiveInt: positive int (x > 0) port of postgresql.
    POSTGRES_PORT: PositiveInt
    #: str: Postgresql user.
    POSTGRES_USER: str
    #: SecretStr: Postgresql password.
    POSTGRES_PASSWORD: SecretStr
    #: str: Postgresql database name.
    POSTGRES_DATABASE_NAME: str

    #: SecretStr: Key for encrypt payload in jwt.
    JWT_SECRET_KEY: SecretStr
    #: str: Access token name in headers/body/cookies.
    JWT_ACCESS_TOKEN_NAME: str
    #: str: Refresh token name in headers/body/cookies.
    JWT_REFRESH_TOKEN_NAME: str

    #: StrictStr: Level of logging which outs in std
    LOGGER_LEVEL: pydantic.StrictStr
    #: pathlib.Path: Path of saving logs on local storage.
    LOGGER_CONFIG_PATH: pathlib.Path


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
