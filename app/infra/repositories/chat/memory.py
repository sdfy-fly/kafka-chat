from dataclasses import dataclass, field

from app.domain.entities.chat import Chat
from app.infra.repositories.chat.base import BaseChatRepository


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def is_chat_exists(self, title: str) -> bool:
        return any(chat for chat in self._saved_chats if chat.title.as_genetic_type() == title)

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)
