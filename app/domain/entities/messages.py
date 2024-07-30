from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.messages import Text


@dataclass(eq=False)
class Message(BaseEntity):  # noqa
    text: Text
