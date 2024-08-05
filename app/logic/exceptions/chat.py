from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class ChatAlreadyExists(LogicException):
    title: str

    @property
    def message(self):
        return f'Chat with name "{self.title}" already exists!'


@dataclass(frozen=True, eq=False)
class ChatNotFound(LogicException):
    chat_oid: str

    @property
    def message(self):
        return f'Chat with oid: {self.chat_oid} not found!'
