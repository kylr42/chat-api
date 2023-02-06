from typing import List

from app.internal.repository.postgresql import message, user_room_mapping
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.exceptions.message import MessageDoesNotBelongToUser
from app.pkg.models.exceptions.repository import EmptyResult
from app.pkg.models.exceptions.room import RoomDoesNotExist

__all__ = ["MessageService"]


class MessageService:
    #: message.MessageRepository: MessageRepository repository implementation.
    repository: message.MessageRepository

    #: message.UserRoomMappingRepository: UserRoomMappingRepository repository implementation.
    user_room_mapping_repository: user_room_mapping.UserRoomMappingRepository

    def __init__(
        self,
        message_repository: BaseRepository,
        user_room_mapping_repository: BaseRepository,
    ):
        self.repository = message_repository
        self.user_room_mapping_repository = user_room_mapping_repository

    async def create_message(
        self,
        cmd: models.CreateMessageCommand,
    ) -> models.Message:
        """Service for saving message to database.

        Args:
            cmd (models.CreateMessageCommand): CreateMessageCommand command.

        Returns:
            models.Message: Message model.
        """
        try:
            await self.user_room_mapping_repository.read_by_room_id_and_user_id(
                query=models.ReadUserRoomMappingByRoomIdAndUserIdQuery(
                    room_id=cmd.room_id,
                    user_id=cmd.user_id,
                ),
            )
        except EmptyResult:
            raise RoomDoesNotExist

        return await self.repository.create(cmd=cmd)

    async def read_message(
        self,
        query: models.ReadMessageQuery,
    ) -> models.Message:
        """Service for reading message from database.

        Args:
            query (models.ReadMessageQuery): ReadMessageQuery query.

        Returns:
            models.Message: Message model.
        """
        return await self.repository.read(query=query)

    async def read_all_room_messages(
        self,
        query: models.ReadAllRoomMessagesQuery,
    ) -> List[models.Message]:
        """Service for reading all messages from database.

        Args:
            query (models.ReadAllRoomMessagesQuery): ReadAllRoomMessagesQuery query.

        Returns:
            List[models.Message]: List of Message models.
        """
        try:
            await self.user_room_mapping_repository.read_by_room_id_and_user_id(
                query=models.ReadUserRoomMappingByRoomIdAndUserIdQuery(
                    room_id=query.room_id,
                    user_id=query.user_id,
                ),
            )
        except EmptyResult:
            raise RoomDoesNotExist

        return await self.repository.read_all_room_messages(query=query)

    async def update_message(
        self,
        cmd: models.UpdateMessageCommand,
    ) -> models.Message:
        """Service for updating message in database.

        Args:
            cmd (models.UpdateMessageCommand): UpdateMessageCommand command.

        Returns:
            models.Message: Message model.
        """
        return await self.repository.update(cmd=cmd)

    async def delete_message(
        self,
        cmd: models.DeleteMessageCommand,
    ) -> models.Message:
        """Service for deleting message from database.

        Args:
            cmd (models.DeleteMessageCommand): DeleteMessageCommand command.

        Returns:
            models.Message: Message model.
        """
        __message = await self.repository.read(query=models.ReadMessageQuery(id=cmd.id))
        if __message.user_id != cmd.user_id:
            raise MessageDoesNotBelongToUser

        return await self.repository.delete(cmd=cmd)
