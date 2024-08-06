from dataclasses import dataclass

from app.domain.entities.messages import Message
from app.infra.repositories.base import BaseMongoRepository
from app.infra.repositories.converters import convert_message_to_document, convert_message_document_to_entity
from app.infra.repositories.message.base import BaseMessageRepository


@dataclass
class MongoMessageRepository(BaseMessageRepository, BaseMongoRepository):

    async def add_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.update_one(
            filter={'oid': chat_oid},
            update={
                '$push': {
                    'messages': convert_message_to_document(message)
                }
            }
        )

    async def get_messages(self, chat_oid: str) -> list[Message] | None:
        result = await self._collection.find_one(filter={'oid': chat_oid})

        if not result:
            return None

        return [
            convert_message_document_to_entity(message_document)
            for message_document in result['messages']
        ]
