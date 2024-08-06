from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any


@dataclass(frozen=True)
class BaseCommand:
    ...


CT = TypeVar('CT', bound=BaseCommand)  # Command Type
CR = TypeVar('CR', bound=Any)


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
