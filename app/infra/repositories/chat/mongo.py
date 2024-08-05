from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from app.domain.entities.chat import Chat
from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.chat.converters import convert_chat_entity_to_document
from app.settings.config import settings


@dataclass
class MongoChatRepository(BaseChatRepository):
    client: AsyncIOMotorClient
    db_name: str
    collection_name: str

    def _get_chat_collection(self) -> AsyncIOMotorCollection:
        return self.client[self.db_name][self.collection_name]

    async def is_chat_exists(self, title: str) -> bool:
        collection = self._get_chat_collection()

        return await collection.find_one(
            filter={'title': title}
        )

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_chat_collection()
        document = convert_chat_entity_to_document(chat)
        await collection.insert_one(document)


def get_chat_mongodb_repository() -> MongoChatRepository:
    client = AsyncIOMotorClient(
        settings.mongo.connection_uri,
        serverselectiontimeoutms=3000
    )

    return MongoChatRepository(
        client=client,
        db_name=settings.mongo.chat.database,
        collection_name=settings.mongo.chat.collection
    )
