from typing import Optional

from aiohttp import web
from socketio import AsyncServer

from server.internal.pkg.middlewares.handle_socket_exceptions import (
    handle_internal_socket_exceptions,
)
from server.internal.routes import __events__
from server.pkg.logger import logger

__all__ = ["SocketServer"]


class SocketServer:
    """Socket server instance."""

    __server: Optional[AsyncServer] = None
    __app: Optional[web.Application] = None

    def __init__(self):
        self.__register_middlewares()
        self.__register_events()

    @property
    def server(self) -> AsyncServer:
        """Get current socket server instance."""
        if not self.__server:
            self.__server = AsyncServer(
                cors_allowed_origins=["*"],
            )
        return self.__server

    @property
    def app(self):
        """Get current socket app instance."""
        if not self.__app:
            self.__app = web.Application(
                logger=logger,
            )
            self.server.attach(
                app=self.__app,
            )
        return self.__app

    def __register_events(self):
        """Register socket events."""
        __events__.register_events(self.server)

    @staticmethod
    def __register_middlewares():
        """Register socket middleware."""
        __events__.register_middleware(handle_internal_socket_exceptions)
