from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Type

from app.domain.events.base import BaseEvent
from app.logic.commands.base import BaseCommandHandler, CT, CR, BaseCommand
from app.logic.events.base import EventHandler, ET, ER
from app.logic.exceptions.mediator import (
    EventHandlersNotRegistered,
    CommandHandlersNotRegistered,
    QueryHandlerNotRegistered
)
from app.logic.queries.base import QT, BaseQueryHandler, QR, BaseQuery


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    commands_map: dict[CT, list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True
    )

    query_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True
    )

    def register_event(
            self,
            event: Type[ET],
            event_handlers: Iterable[EventHandler[ET, ER]]
    ):
        self.events_map[event].extend(event_handlers)

    def register_command(
            self,
            command: Type[CT],
            command_handlers: Iterable[BaseCommandHandler[CT, CR]]
    ):
        self.commands_map[command].extend(command_handlers)

    def register_query(
            self,
            query: Type[QT],
            query_handler: BaseQueryHandler[QT, QR]
    ):
        self.query_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> list[ER]:
        result = []

        for event in events:
            data: list[ER] = await self.__handle_event(event)
            result.extend(data)

        return result

    async def handle_command(self, command: BaseCommand) -> list[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegistered(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        query_type = query.__class__
        handler = self.query_map.get(query_type)

        if not handler:
            raise QueryHandlerNotRegistered(query_type)

        return await handler.handle(query)

    async def __handle_event(self, event: BaseEvent) -> list[ER]:
        event_type = event.__class__
        handlers = self.events_map.get(event_type)

        if not handlers:
            raise EventHandlersNotRegistered(event_type)

        return [await handler.handle(event) for handler in handlers]
