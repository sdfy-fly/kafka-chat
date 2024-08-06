from dataclasses import dataclass

from app.domain.entities.chat import Chat
from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.message.base import BaseMessageRepository
from app.logic.exceptions.chat import ChatNotFound
from app.logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass
class GetChatDetailQueryHandler(BaseQueryHandler[GetChatDetailQuery, Chat]):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository

    async def handle(self, query: GetChatDetailQuery) -> Chat:
        chat: Chat = await self.chat_repository.get_chat_by_oid(query.chat_oid)
        if not chat:
            raise ChatNotFound(query.chat_oid)

        return chat
