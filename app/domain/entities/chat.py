from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.entities.messages import Message
from app.domain.values.chat import Title


@dataclass
class Chat(BaseEntity):  # noqa
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    def add_message(self, message: Message):
        self.messages.add(message)
