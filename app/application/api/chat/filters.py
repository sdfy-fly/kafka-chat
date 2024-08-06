from pydantic import BaseModel

from app.infra.repositories.filters.messages import GetMessagesFilter as GetMessagesInfoFilters


class GetMessagesFilter(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self):
        return GetMessagesInfoFilters(limit=self.limit, offset=self.offset)
