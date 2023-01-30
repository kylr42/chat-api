from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.handle_exception import (
    handle_exception,
)
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model

__all__ = ["MessageTypeRepository"]


class MessageTypeRepository(Repository):
    @handle_exception
    async def create(self, cmd: models.CreateMessageTypeCommand) -> None:
        q = """
            insert into message_types(name)
                values (%(name)s) on conflict do nothing
            returning id, name;
        """

        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())

    async def read(self, query: Model) -> Model:
        raise NotImplementedError

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    async def update(self, cmd: Model) -> Model:
        raise NotImplementedError

    async def delete(self, cmd: Model) -> Model:
        raise NotImplementedError
