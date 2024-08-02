from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.entities.messages import Message
from app.domain.events.chat import NewMessageReceivedEvent, NewChatCreated
from app.domain.values.chat import Title


@dataclass
class Chat(BaseEntity):  # noqa
    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True
    )

    @classmethod
    def create(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreated(chat_oid=new_chat.oid, chat_title=new_chat.title.as_genetic_type())
        )

        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_genetic_type(),
            message_oid=message.oid,
            chat_oid=self.oid,
        ))
