from dataclasses import dataclass

from app.domain.entities.chat import Chat
from app.infra.repositories.base import BaseMongoRepository
from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.converters import convert_chat_entity_to_document, convert_chat_document_to_entity


@dataclass
class MongoChatRepository(BaseChatRepository, BaseMongoRepository):

    async def is_chat_exists_by_title(self, title: str) -> bool:
        return bool(
            await self._collection.find_one(filter={'title': title})
        )

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'oid': oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def add_chat(self, chat: Chat) -> None:
        document = convert_chat_entity_to_document(chat)
        await self._collection.insert_one(document)
