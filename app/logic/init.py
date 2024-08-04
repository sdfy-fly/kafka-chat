from functools import lru_cache

from punq import Container, Scope

from app.infra.repositories.chat import BaseChatRepository, MemoryChatRepository
from app.logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()
    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            command=CreateChatCommand,
            command_handlers=[
                container.resolve(CreateChatCommandHandler)
            ]
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
