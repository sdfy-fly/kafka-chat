from pydantic import BaseModel

from app.domain.entities.chat import Chat


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(oid=chat.oid, title=chat.title.as_genetic_type())
