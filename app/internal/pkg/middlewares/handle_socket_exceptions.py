from typing import Callable

from starlette import status

from app.internal.events.chat import router
from app.pkg.logger import logger
from app.pkg.models.base import BaseAPIException

__all__ = [
    "handle_internal_socket_exceptions",
]


def handle_internal_socket_exceptions(func: Callable):
    """Handle all internal unhandled exceptions."""

    async def wrapper(sid: str, *args, **kwargs):
        try:
            return await func(sid, *args, **kwargs)

        except BaseAPIException as exc:
            logger.error(f"BaseAPIException: {exc} {exc.status_code} {exc.message}")
            await router.server.disconnect(sid=sid)

        except Exception as exc:
            logger.error(f"Unhandled exception: {exc} {repr(exc)}")
            await router.server.disconnect(sid=sid)

    return wrapper
