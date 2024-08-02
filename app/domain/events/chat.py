from dataclasses import dataclass

from app.domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):  # noqa
    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreated(BaseEvent):  # noqa
    chat_oid: str
    chat_title: str
