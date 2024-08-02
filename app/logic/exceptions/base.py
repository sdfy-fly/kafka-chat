from dataclasses import dataclass

from app.domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class LogicException(ApplicationException):
    @property
    def message(self):
        return 'Logic exception occurred'
