"""Global point for collected routers."""
from app.internal.pkg.models import Routes
from app.internal.routes import auth, user, profile, message, room

__all__ = ["__routes__"]


__routes__ = Routes(routers=(user.router, auth.router, profile.router, message.router, room.router))
# TODO: Добавить документацию.
