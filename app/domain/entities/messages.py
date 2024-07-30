from dataclasses import dataclass, field
from uuid import uuid4

from app.domain.values.messages import Text


@dataclass
class Message:
    text: Text
    oid: str = field(
        default_factory=lambda: str(uuid4()), kw_only=True
    )
