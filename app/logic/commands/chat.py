from dataclasses import dataclass

from app.domain.entities.chat import Chat
from app.domain.values.chat import Title
from app.infra.repositories.chat.base import BaseChatRepository
from app.logic.commands.base import BaseCommand, CommandHandler
from app.logic.exceptions.messages import ChatAlreadyExists


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    repository: BaseChatRepository

    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.repository.is_chat_exists(command.title):
            raise ChatAlreadyExists(command.title)

        title = Title(value=command.title)
        chat = Chat.create(title)

        await self.repository.add_chat(chat)
        return chat
