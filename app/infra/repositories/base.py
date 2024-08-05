from abc import ABC
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection


@dataclass
class BaseMongoRepository(ABC):
    client: AsyncIOMotorClient
    db_name: str
    collection_name: str

    @property
    def _collection(self) -> AsyncIOMotorCollection:
        return self.client[self.db_name][self.collection_name]
