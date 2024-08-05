from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.chat.mongo import MongoChatRepository
from app.infra.repositories.message.base import BaseMessageRepository
from app.infra.repositories.message.mongo import MongoMessageRepository
from app.logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from app.logic.commands.message import CreateMessageCommandHandler, CreateMessageCommand
from app.logic.mediator import Mediator
from app.settings.config import settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # Mongo
    container.register(AsyncIOMotorClient, factory=get_mongodb_connection, scope=Scope.singleton)

    # Repositories
    container.register(
        BaseChatRepository,
        MongoChatRepository,
        scope=Scope.singleton,
        db_name=settings.mongo.chat.database,
        collection_name=settings.mongo.chat.collection
    )
    container.register(
        BaseMessageRepository,
        MongoMessageRepository,
        scope=Scope.singleton,
        db_name=settings.mongo.chat.database,
        collection_name=settings.mongo.chat.collection
    )

    # Command Handlers
    container.register(CreateChatCommandHandler)
    container.register(CreateMessageCommandHandler)

    # Mediator
    def init_mediator():
        mediator = Mediator()

        mediator.register_command(
            command=CreateChatCommand,
            command_handlers=[
                container.resolve(CreateChatCommandHandler)
            ]
        )

        mediator.register_command(
            command=CreateMessageCommand,
            command_handlers=[
                container.resolve(CreateMessageCommandHandler)
            ]
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container


def get_mongodb_connection():
    return AsyncIOMotorClient(
        settings.mongo.connection_uri,
        serverselectiontimeoutms=3000
    )
