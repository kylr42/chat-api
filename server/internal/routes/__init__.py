from server.internal.pkg.models import Events
from server.internal.routes import connect, message, room

__all__ = ["__events__"]

__events__ = Events(events=(connect.router, room.router, message.router))
