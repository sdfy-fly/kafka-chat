from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.messages import Message
from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.filters.messages import GetMessagesFilter
from app.infra.repositories.message.base import BaseMessageRepository
from app.logic.exceptions.chat import ChatNotFound
from app.logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilter


@dataclass
class GetMessagesQueryHandler(BaseQueryHandler):
    chat_repository: BaseChatRepository
    message_repository: BaseMessageRepository

    async def handle(self, query: GetMessagesQuery) -> tuple[Iterable[Message], int]:
        chat = await self.chat_repository.get_chat_by_oid(query.chat_oid)
        if not chat:
            raise ChatNotFound(query.chat_oid)

        messages, count = await self.message_repository.get_messages(
            chat_oid=chat.oid, filters=query.filters
        )
        return messages, count
