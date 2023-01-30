from typing import List

from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.internal.repository.postgresql import message

__all__ = ["MessageService"]


class MessageService:
    #: message.MessageRepository: MessageRepository repository implementation.
    repository: message.MessageRepository

    def __init__(self, message_repository: BaseRepository):
        self.repository = message_repository

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