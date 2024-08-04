from punq import Container, Scope

from app.infra.repositories.chat import BaseChatRepository, MemoryChatRepository
from app.logic.init import _init_container


def init_test_container() -> Container:
    container = _init_container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    
    return container
