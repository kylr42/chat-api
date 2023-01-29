"""Model for contain ``APIRouter`` instance."""

from typing import Any, Callable, Dict, List, Optional

from socketio import AsyncServer

__all__ = ["SocketRoutes"]


class SocketRoutes:
    routes: List[str] = []
    __routes__: Dict[str, Any] = {}
    __server__: Optional[AsyncServer] = None

    def on(self, event: Optional[str] = None, *args, **kwargs) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes.append(event if event else func.__name__)
            self.__routes__[event if event else func.__name__] = {
                "func": func,
                "args": args,
                "kwargs": kwargs,
            }
            return func

        return decorator

    @property
    def server(self) -> AsyncServer:
        if not self.__server__:
            raise ValueError("Server not initialized")
        return self.__server__

    @server.setter
    def server(self, server: AsyncServer):
        if not isinstance(server, AsyncServer):
            raise TypeError("Server must be instance of AsyncServer")

        self.__server__ = server

        for event in self.routes:
            self.__server__.on(
                event,
                handler=self.__routes__[event]["func"],
                *self.__routes__[event]["args"],
                **self.__routes__[event]["kwargs"],
            )
