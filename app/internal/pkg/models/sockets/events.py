"""Model for contain ``APIRouter`` instance."""

from dataclasses import dataclass
from typing import Tuple

from socketio import AsyncServer

from app.internal.pkg.models.sockets.routes import SocketRoutes

__all__ = ["Events"]


@dataclass(frozen=True)
class Events:
    events: Tuple[SocketRoutes, ...]

    def register_events(self, server: AsyncServer):
        for router in self.events:
            router.server = server
