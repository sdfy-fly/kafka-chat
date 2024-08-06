from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.messages import Message
from app.infra.repositories.base import BaseMongoRepository
from app.infra.repositories.converters import convert_message_to_document, convert_message_document_to_entity
from app.infra.repositories.filters.messages import GetMessagesFilter
from app.infra.repositories.message.base import BaseMessageRepository


@dataclass
class MongoMessageRepository(BaseMessageRepository, BaseMongoRepository):

    async def add_message(self, message: Message) -> None:
        await self._collection.insert_one(document=convert_message_to_document(message))

    async def get_messages(self, filters: GetMessagesFilter, chat_oid: str) -> tuple[Iterable[Message], int]:
        query = {'chat_oid': chat_oid}
        cursor = (
            self._collection
            .find(filter=query)
            .limit(filters.limit)
            .skip(filters.offset)
            .sort('created_at')
        )
        
        count = await self._collection.count_documents(query)
        messages = [
            convert_message_document_to_entity(message_document)
            async for message_document in cursor
        ]

        return messages, count
