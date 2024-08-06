from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EventHandlersNotRegistered(LogicException):
    event_type: type

    @property
    def message(self):
        return f'Could not find handler for event: {self.event_type}'


@dataclass(frozen=True, eq=False)
class CommandHandlersNotRegistered(LogicException):
    command_type: type

    @property
    def message(self):
        return f'Could not find handler for command: {self.command_type}'


@dataclass(frozen=True, eq=False)
class QueryHandlerNotRegistered(LogicException):
    query_type: type

    @property
    def message(self):
        return f'Could not find handler for query: {self.query_type}'
