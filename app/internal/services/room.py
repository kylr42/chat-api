import typing
from typing import List

from app.internal.repository.postgresql import RoomRepository, UserRoomMappingRepository
from app.internal.repository.repository import BaseRepository
from app.pkg import models

__all__ = ["RoomService"]


class RoomService:
    repository: RoomRepository
    user_room_mapping_repository: UserRoomMappingRepository

    def __init__(
        self,
        room_repository: typing.Type[BaseRepository],
        user_room_mapping_repository: typing.Type[BaseRepository],
    ):
        self.repository = room_repository
        self.user_room_mapping_repository = user_room_mapping_repository

    async def create_room(self, cmd: models.CreateRoomCommand) -> models.Room:
        """Method for create room.

        Args:
            cmd: `CreateRoomRequest`.

        Returns: `Room` model.
        """
        room = await self.repository.create(
            cmd=models.CreateRoomCommand(
                name=cmd.name,
                description=cmd.description,
            ),
        )
        room_user_mapping = await self.user_room_mapping_repository.create(
            cmd=models.CreateUserRoomMappingCommand(
                user_id=cmd.user_id,
                room_id=room.id,
            ),
        )
        return models.Room(
            id=room.id,
            name=room.name,
            description=room.description,
            is_archived=room_user_mapping.is_archived,
            is_favorite=room_user_mapping.is_favorite,
        )

    async def read_all_user_rooms(
        self, query: models.ReadAllUserRoomsQuery
    ) -> List[models.Room]:
        """Read all user rooms from repository.

        Args:
            query: `ReadAllUserRoomsQuery`.

        Returns: `Room` model.
        """
        return await self.repository.read_all_user_rooms(query=query)

    async def read_specific_room_by_id(
        self, query: models.ReadRoomByIdQuery
    ) -> models.Room:
        """Read specific room from repository by room id.

        Args:
            query: `ReadRoomByIdQuery`.

        Returns: `Room` model.
        """
        return await self.repository.read(query=query)

    async def update_room(self, cmd: models.UpdateRoomCommand) -> models.Room:
        """Update room in repository.

        Args:
            cmd: `UpdateRoomCommand`.

        Returns: `Room` model.
        """
        return await self.repository.update(cmd=cmd)

    async def update_status_room(
        self,
        cmd: models.UpdateUserRoomMappingStatusCommand,
    ) -> models.Room:
        """Update status room in repository.

        Args:
            cmd: `UpdateStatusRoomCommand`.

        Returns: `Room` model.
        """
        user_room_mapping = await self.user_room_mapping_repository.update_room_status(
            cmd=cmd,
        )
        return await self.repository.read(
            query=models.ReadRoomByIdQuery(id=user_room_mapping.room_id),
        )

    async def delete_room(self, cmd: models.DeleteRoomCommand) -> models.Room:
        """Delete room in repository.

        Args:
            cmd: `DeleteRoomCommand`.

        Returns: `Room` model.
        """
        user_room_mappings = await self.user_room_mapping_repository.read_by_room_id(
            query=models.ReadUserRoomMappingByRoomIdQuery(room_id=cmd.id),
        )
        for user_room_mapping in user_room_mappings:
            await self.user_room_mapping_repository.delete(
                cmd=models.DeleteUserRoomMappingCommand(id=user_room_mapping.id),
            )

        return await self.repository.delete(cmd=cmd)

    async def add_user_to_room(self, cmd: models.AddUserToRoomCommand) -> models.Room:
        """Add user to room in repository.

        Args:
            cmd: `AddUserToRoomCommand`.

        Returns: `Room` model.
        """
        await self.user_room_mapping_repository.create(
            cmd=models.CreateUserRoomMappingCommand(
                user_id=cmd.user_id,
                room_id=cmd.room_id,
            ),
        )
        return await self.repository.read(
            query=models.ReadRoomByIdQuery(
                id=cmd.room_id,
                user_id=cmd.user_id,
            ),
        )

    async def read_all_rooms_of_user(
        self,
        query: models.ReadAllUserRoomsQuery,
    ) -> List[models.Room]:
        """Read all rooms of user from repository.

        Args:
            query: `ReadAllUserRoomsQuery`.

        Returns: `Room` model.
        """

        return await self.repository.read_all_user_rooms(query=query)

    async def update_user_room_mapping(
        self,
        cmd: models.UpdateUserRoomMappingCommand,
    ) -> models.UserRoomMapping:
        """Update user room mapping in repository.

        Args:
            cmd: `UpdateUserRoomMappingCommand`.

        Returns: `UserRoomMapping` model.
        """
        return await self.user_room_mapping_repository.update(cmd=cmd)

    async def delete_user_room_mapping(
        self,
        cmd: models.DeleteUserRoomMappingCommand,
    ) -> models.UserRoomMapping:
        """Delete user room mapping in repository.

        Args:
            cmd: `DeleteUserRoomMappingCommand`.

        Returns: `UserRoomMapping` model.
        """
        return await self.user_room_mapping_repository.delete(cmd=cmd)
