from dataclasses import dataclass

from app.domain.exceptions.messages import TextTooLongException, EmptyTextException
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise TextTooLongException(self.value)

    def as_genetic_type(self) -> str:
        return str(self.value)
