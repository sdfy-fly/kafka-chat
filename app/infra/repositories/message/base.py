from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from app.domain.entities.messages import Message
from app.infra.repositories.filters.messages import GetMessagesFilter


@dataclass
class BaseMessageRepository(ABC):
    @abstractmethod
    async def add_message(self, message: Message) -> None:
        ...

    @abstractmethod
    async def get_messages(self, filters: GetMessagesFilter, chat_oid: str) -> tuple[Iterable[Message], int]:
        ...
