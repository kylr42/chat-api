from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models

__all__ = ["RoomRepository"]


class RoomRepository(Repository):
    @collect_response
    async def create(self, cmd: models.CreateRoomCommand) -> models.Room:
        q = """
            insert into rooms(
                name, description
            ) values (
                %(name)s,
                %(description)s
            )
            returning id, name, description;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadRoomByIdQuery) -> models.Room:
        q = """
            with room_status as (
                select
                    room_id, is_archived, is_favorite
                from user_room_mapping
                where room_id = %(id)s and user_id = %(user_id)s
            )
            select
                id,
                name,
                description,
                rs.is_archived as is_archived,
                rs.is_favorite as is_favorite
            from rooms
                left join room_status as rs on rooms.id = rs.room_id
            where rooms.id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_all_user_rooms(
        self,
        query: models.ReadAllUserRoomsQuery,
    ) -> List[models.Room]:
        q = """
            select
                rooms.id as id,
                is_archived,
                is_favorite,
                rooms.name as name,
                rooms.description as description
            from user_room_mapping
                left join rooms on user_room_mapping.room_id = rooms.id
            where user_room_mapping.user_id = %(user_id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    async def read_all(self):
        raise NotImplementedError

    @collect_response
    async def update(self, cmd: models.UpdateRoomCommand) -> models.Room:
        q = """
            with rs as (
                select
                    is_archived, is_favorite
                 where room_id = %(id)s and user_id = %(user_id)s
            )
            update rooms
                set
                    name = %(name)s,
                    description = %(description)s
                where id = %(id)s
            returning id, name, description, rs.is_archived, rs.is_favorite;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteRoomCommand) -> models.Room:
        q = """
            delete from rooms
            where id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
