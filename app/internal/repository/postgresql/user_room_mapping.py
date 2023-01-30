from typing import List

from app.internal.repository.postgresql.connection import get_connection
from app.internal.repository.postgresql.handlers.collect_response import (
    collect_response,
)
from app.internal.repository.repository import Repository
from app.pkg import models
from app.pkg.models.base import Model

__all__ = ["UserRoomMappingRepository"]


class UserRoomMappingRepository(Repository):
    @collect_response
    async def create(self, cmd: models.CreateUserRoomMappingCommand) -> models.UserRoomMapping:
        q = """
            insert into user_room_mapping(
                user_id, room_id
            ) values (
                %(user_id)s,
                %(room_id)s
            )
            returning id, user_id, room_id, is_archived, is_favorite;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read(self, query: models.ReadUserRoomMappingByIdQuery) -> models.UserRoomMapping:
        q = """
            select
                id,
                user_id,
                room_id,
                is_archived,
                is_favorite
            from user_room_mapping
            where user_room_mapping.id = %(id)s;
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchone()

    @collect_response
    async def read_by_room_id(
        self,
        query: models.ReadUserRoomMappingByRoomIdQuery,
    ) -> List[models.UserRoomMapping]:
        q = """
            select
                id, user_id, room_id, is_archived, is_favorite
            from user_room_mapping
            where user_room_mapping.room_id = %(room_id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    @collect_response
    async def read_all_user_rooms(self, query: models.ReadUserRoomMappingByUserIdQuery) -> List[models.UserRoomMapping]:
        q = """
            select
                id, user_id, room_id, is_archived, is_favorite
            from user_room_mapping
            where user_room_mapping.user_id = %(user_id)s
        """
        async with get_connection() as cur:
            await cur.execute(q, query.to_dict())
            return await cur.fetchall()

    async def read_all(self) -> List[Model]:
        raise NotImplementedError

    @collect_response
    async def update(self, cmd: models.UpdateUserRoomMappingCommand) -> models.UserRoomMapping:
        q = """
            update user_room_mapping
                set 
                    chat_id = %(chat_id)s,
                    room_id = %(room_id)s
                where id = %(id)s
            returning id, user_id, room_id, is_archived, is_favorite;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def update_room_status(
        self, cmd: models.UpdateUserRoomMappingStatusCommand
    ) -> models.UserRoomMapping:
        q = """
            update user_room_mapping
                set
                    is_archived = %(is_archived)s,
                    is_favorite = %(is_favorite)s
                where id = %(id)s
            returning id, user_id, room_id, is_archived, is_favorite;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()

    @collect_response
    async def delete(self, cmd: models.DeleteUserRoomMappingCommand) -> models.UserRoomMapping:
        q = """
            delete from user_room_mapping where id = %(id)s
            returning id, user_id, room_id, is_archived, is_favorite;
        """
        async with get_connection() as cur:
            await cur.execute(q, cmd.to_dict())
            return await cur.fetchone()
