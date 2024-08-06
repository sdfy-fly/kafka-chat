from typing import TypeVar, Generic

from pydantic import BaseModel

R = TypeVar('R', bound=BaseModel)


class ErrorSchema(BaseModel):
    error: str


class BaseQueryResponse(BaseModel, Generic[R]):
    items: R
    count: int
    offset: int
    limit: int
