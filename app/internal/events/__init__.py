from app.internal.events import chat, connect
from app.internal.pkg.models.sockets import Events

__all__ = ["__events__"]

__events__ = Events(events=(chat.router, connect.router))
