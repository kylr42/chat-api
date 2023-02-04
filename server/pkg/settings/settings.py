"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""
import pathlib
from functools import lru_cache

import pydantic
from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings

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

    #: StrictStr: Level of logging which outs in std
    LOGGER_LEVEL: pydantic.StrictStr
    #: pathlib.Path: Path to logging config file in json format (see `logging.config.dictConfig`)
    LOGGER_CONFIG_FILE: pathlib.Path

    #: str: Base url for backend service
    CHAT_API_BASE_URL: pydantic.AnyUrl


@lru_cache()
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
