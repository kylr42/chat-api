from app.internal.events import room, connect
from app.internal.pkg.models.sockets import Events

__all__ = ["__events__"]

__events__ = Events(events=(room.router, connect.router))
