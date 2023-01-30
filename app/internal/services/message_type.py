import typing

from app.internal.repository.postgresql import message_type
from app.internal.repository.repository import BaseRepository
from app.pkg import models
from app.pkg.models.base import BaseAPIException
from app.pkg.models.exceptions.repository import DriverError, UniqueViolation

__all__ = ["MessageTypeService"]


class MessageTypeService:
    #: message_type.MessageTypeRepository: MessageTypeRepository repository implementation.
    repository: message_type.MessageTypeRepository

    def __init__(self, message_type_repository: BaseRepository):
        self.repository = message_type_repository

    async def create_all_message_types(
        self,
    ) -> typing.AsyncIterable[typing.Optional[BaseAPIException]]:
        for type_name in models.MessageType:
            try:
                await self.repository.create(
                    cmd=models.CreateMessageTypeCommand(name=type_name),
                )
            except DriverError as e:
                yield e
            except UniqueViolation:
                continue
