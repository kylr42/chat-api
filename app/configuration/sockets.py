from typing import Optional

from socketio import ASGIApp, AsyncServer

from app.internal.events import __events__

__all__ = ["SocketServer"]


class SocketServer:
    """Socket server instance."""

    __server: Optional[AsyncServer] = None
    __app: Optional[ASGIApp] = None

    def __init__(self):
        self.__register_events()

    @property
    def server(self) -> AsyncServer:
        """Get current socket server instance."""
        if not self.__server:
            self.__server = AsyncServer(
                async_mode="asgi",
                cors_allowed_origins=["*"],
            )
        return self.__server

    @property
    def app(self):
        """Get current socket app instance."""
        if not self.__app:
            self.__app = ASGIApp(
                socketio_server=self.server,
                socketio_path="/socket.io",
            )
        return self.__app

    def __register_events(self):
        """Register socket events."""
        __events__.register_events(self.server)
