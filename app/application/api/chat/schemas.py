from datetime import datetime

from pydantic import BaseModel

from app.domain.entities.chat import Chat
from app.domain.entities.messages import Message


class CreateChatSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(oid=chat.oid, title=chat.title.as_genetic_type())


class CreateMessageSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str

    @classmethod
    def from_entity(cls, message: Message) -> 'CreateMessageResponseSchema':
        return cls(oid=message.oid, text=message.text.as_genetic_type())


class MessageSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> 'MessageSchema':
        return cls(oid=message.oid, text=message.text.as_genetic_type(), created_at=message.created_at)


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: Chat) -> 'ChatDetailSchema':
        return cls(oid=chat.oid, title=chat.title.as_genetic_type(), created_at=chat.created_at)
