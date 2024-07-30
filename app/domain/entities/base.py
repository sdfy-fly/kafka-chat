from abc import ABC
from dataclasses import field, dataclass
from datetime import datetime
from uuid import uuid4


@dataclass
class BaseEntity(ABC):
    oid: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True
    )

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True
    )

    def __hash__(self):
        return hash(self.oid)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.oid == __value.oid
