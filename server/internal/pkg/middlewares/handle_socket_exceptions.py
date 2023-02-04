"""Handle all internal unhandled exceptions.

Examples:
    For example, if in some level in code you raise error inherited by
    BaseAPIException::

    ...  # exceptions.py
    class E(BaseAPIException):
        status_code = status.HTTP_200_OK
        message = "test error."

    ...  # some_file.py
    async def some_internal_function():
        raise E

    When `some_internal_function` called, exception will process by
    ``handle_api_exceptions`` and returns json object::

    {
        "message": "test error."
    }
"""


from typing import Callable

from server.internal.routes.connect import router
from server.pkg.logger import logger
from server.pkg.models.base import BaseAPIException

__all__ = [
    "handle_internal_socket_exceptions",
]


def handle_internal_socket_exceptions(func: Callable):
    """Handle all internal unhandled exceptions."""

    async def wrapper(sid: str, *args, **kwargs):
        try:
            return await func(sid, *args, **kwargs)

        except BaseAPIException as exc:
            logger.error(f"BaseAPIException: {exc.message}")
            await router.server.emit(
                event="error",
                data=exc.message,
                room=sid,
            )
            await router.server.disconnect(sid)

        except Exception as exc:
            logger.critical(f"Unhandled exception: {exc} {repr(exc)}")
            await router.server.emit(
                event="error",
                data=repr(exc),
                room=sid,
            )
            await router.server.disconnect(sid)

    return wrapper
