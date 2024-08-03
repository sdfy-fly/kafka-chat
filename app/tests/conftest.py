import pytest

from app.infra.repositories.chat import MemoryChatRepository, BaseChatRepository
from app.logic.init import init_mediator
from app.logic.mediator import Mediator


@pytest.fixture(scope='function')
def chat_repository() -> MemoryChatRepository:
    return MemoryChatRepository()


@pytest.fixture(scope='function')
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator
