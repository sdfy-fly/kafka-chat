from dataclasses import dataclass

from app.domain.entities.messages import Message
from app.infra.repositories.base import BaseMongoRepository
from app.infra.repositories.converters import convert_message_to_document
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
