from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass
class TextTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Message text too long "{self.text[:100]}..."'


@dataclass
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return f'Message text could not be empty'
