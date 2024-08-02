from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class ChatAlreadyExists(LogicException):
    title: str

    @property
    def message(self):
        return f'Chat with name "{self.title}" already exists!'
