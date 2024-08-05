from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.chat import Chat


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def is_chat_exists(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...
