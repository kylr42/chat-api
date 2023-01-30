from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["MessageRepository"]


class MessageRepository(Repository):
    @collect_response
    async def create(self, cmd: models.CreateMessageCommand) -> models.Message:
        q = """
            insert into messages(
                room_id, user_id, message, message_type_id
            ) values (
                %(room_id)s, %(user_id)s, %(text)s, %(message_type_id)s
            )
            returning
                id, room_id, user_id, message as text, (
                    select name from message_types where id = 1
                ) as message_type_name;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadMessageQuery) -> models.Message:
        q = """
            select
                id, room_id, user_id, message as text, mt.name as message_type_name
            from messages
                left join message_types mt on messages.message_type_id = mt.id
            where id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all_room_messages(
        self, query: models.ReadAllRoomMessagesQuery
    ) -> List[models.Message]:
        q = """
            select
                id, room_id, user_id, message as text, mt.name as message_type_name
            from messages
                left join message_types mt on messages.message_type_id = mt.id
            where room_id = %(room_id)s
            limit %(limit)s offset %(offset)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    async def read_all(self):
        raise NotImplementedError

    @collect_response
    async def update(self, cmd: models.UpdateMessageCommand) -> models.Message:
        q = """
            with mt as (
                select id, name from message_types where id = %(message_type_id)s
            )
            update messages
            set
                text = %(text)s
            where id = %(id)s
            returning id, room_id, user_id, message as text, mt.name as message_type_name;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteRoomCommand) -> models.Room:
        q = """
            delete from rooms
            where id = %(id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
