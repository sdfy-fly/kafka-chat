from dataclasses import dataclass, field

from app.domain.entities.chat import Chat
from app.infra.repositories.chat.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def is_chat_exists_by_title(self, title: str) -> bool:
        return any(chat for chat in self._saved_chats if chat.title.as_genetic_type() == title)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:

        if chats := [chat for chat in self._saved_chats if chat.oid == oid]:
            return chats[0]

        return None

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
