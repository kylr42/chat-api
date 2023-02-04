"""Model for contain ``APIRouter`` instance.

Examples:

    For register routes, you **must** provide events to model.::

        from routers import users, auth
        __events__ = Events(
            events=(
                users.event,
                auth.event
            )
        )

    If you call ``register_routes``, all routes from *self.routers* will be
    included to the ``AsyncServer`` instance.::

        from socketio import AsyncServer

        server = AsyncServer()
        __events__.register_events(server=server)
"""

from dataclasses import dataclass
from typing import Callable, Tuple

from socketio import AsyncServer

from server.internal.pkg.models.routes import SocketRoutes

__all__ = ["Events"]


@dataclass(frozen=True)
class Events:
    events: Tuple[SocketRoutes, ...]

    def register_events(self, server: AsyncServer):
        """Include ``APIRouter`` to the ``AsyncServer`` application instance.

        Args:
            server: ``AsyncServer`` application instance.
        """
        for router in self.events:
            router.server = server

    def register_middleware(self, middleware: Callable):
        """Register middleware for all events.

        Args:
            middleware: Callable middleware.
        """
        for router in self.events:
            router.register_middleware(middleware)
