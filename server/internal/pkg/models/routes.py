"""Model for contain ``APIRouter`` instance."""

from typing import Any, Callable, Dict, List, Optional, Tuple

from socketio import AsyncServer

__all__ = ["SocketRoutes"]


class SocketRoutes:
    __routes__: Dict[str, Any] = {}
    __middlewares__: List[Callable] = []
    __server__: Optional[AsyncServer] = None

    def on(
        self,
        event: Optional[str] = None,
        *args: Tuple[Any],
        **kwargs: Dict[str, Any],
    ) -> Callable:
        """Register socket event."""

        def decorator(func: Callable) -> Callable:
            """Decorator for register socket event."""
            event_name = event or func.__name__

            self.__routes__[event_name] = {
                "func": func,
                "args": args,
                "kwargs": kwargs,
            }
            return func

        return decorator

    @property
    def server(self) -> AsyncServer:
        """Get current socket server instance."""
        if not self.__server__:
            raise ValueError("Server not initialized")
        return self.__server__

    @server.setter
    def server(self, server: AsyncServer):
        """Set current socket server instance."""
        if not isinstance(server, AsyncServer):
            raise TypeError("Server must be instance of AsyncServer")

        self.__server__ = server

        for event, value in self.__routes__.items():
            self.__server__.on(
                event,
                handler=self.__register_middleware__(
                    func=value["func"],
                ),
                *value["args"],
                **value["kwargs"],
            )

    def __register_middleware__(
        self,
        func: Callable,
        middlewares: Optional[List[Callable]] = None,
    ) -> Callable:
        """Register socket middleware."""
        if not middlewares:
            middlewares = self.__middlewares__

        for middleware in middlewares:
            func = middleware(func)
        return func

    def register_middleware(self, middleware: Callable):
        """Register socket middleware."""
        self.__middlewares__.append(middleware)
