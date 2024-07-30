from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass
class TitleTooLongException(ApplicationException):
    title: str

    @property
    def message(self):
        return f'Chat title too long "{self.title[:100]}"...'


@dataclass
class EmptyTitleException(ApplicationException):
    @property
    def message(self):
        return f'Chat title could not be empty'
