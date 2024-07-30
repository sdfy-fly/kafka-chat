from dataclasses import dataclass

from app.domain.exceptions.chat import TitleTooLongException, EmptyTitleException
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTitleException()

        if len(self.value) > 100:
            raise TitleTooLongException(self.value)

    def as_genetic_type(self):
        return str(self.value)
