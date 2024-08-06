from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.chat.mongo import MongoChatRepository
from app.infra.repositories.message.base import BaseMessageRepository
from app.infra.repositories.message.mongo import MongoMessageRepository
from app.logic.commands.chat import CreateChatCommand, CreateChatBaseCommandHandler
from app.logic.commands.messages import CreateMessageBaseCommandHandler, CreateMessageCommand
from app.logic.mediator import Mediator
from app.logic.queries.chat import GetChatDetailQueryHandler, GetChatDetailQuery
from app.logic.queries.messages import GetMessagesQuery, GetMessagesQueryHandler
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
        collection_name=settings.mongo.chat.chat_collection
    )
    container.register(
        BaseMessageRepository,
        MongoMessageRepository,
        scope=Scope.singleton,
        db_name=settings.mongo.chat.database,
        collection_name=settings.mongo.chat.message_collection
    )

    # Command Handlers
    container.register(CreateChatBaseCommandHandler)
    container.register(CreateMessageBaseCommandHandler)

    # Query Handlers
    container.register(GetChatDetailQueryHandler)
    container.register(GetMessagesQueryHandler)

    # Mediator
    def init_mediator():
        mediator = Mediator()

        mediator.register_command(
            command=CreateChatCommand,
            command_handlers=[
                container.resolve(CreateChatBaseCommandHandler)
            ]
        )

        mediator.register_command(
            command=CreateMessageCommand,
            command_handlers=[
                container.resolve(CreateMessageBaseCommandHandler)
            ]
        )

        mediator.register_query(
            query=GetChatDetailQuery,
            query_handler=container.resolve(GetChatDetailQueryHandler)
        )
        mediator.register_query(
            query=GetMessagesQuery,
            query_handler=container.resolve(GetMessagesQueryHandler)
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container


def get_mongodb_connection():
    return AsyncIOMotorClient(
        settings.mongo.connection_uri,
        serverselectiontimeoutms=3000
    )
