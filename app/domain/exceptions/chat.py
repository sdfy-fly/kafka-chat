from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class TitleTooLongException(ApplicationException):
    title: str

    @property
    def message(self):
        return f'Chat title too long "{self.title[:100]}"...'


@dataclass(frozen=True, eq=False)
class EmptyTitleException(ApplicationException):
    @property
    def message(self):
        return f'Chat title could not be empty'
