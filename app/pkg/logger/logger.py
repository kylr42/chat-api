import json
import logging.config

from app.pkg.settings import settings

__all__ = [
    "get_logger",
]


def get_logger(name):
    with open(settings.LOGGER_CONFIG_PATH, "r") as fd:
        logging.config.dictConfig(config=json.load(fd))
    logger = logging.getLogger(name)
    return logger
