from dataclasses import dataclass

from app.domain.entities.messages import Message
from app.domain.values.messages import Text
from app.infra.repositories.chat.base import BaseChatRepository
from app.infra.repositories.message.base import BaseMessageRepository
from app.logic.commands.base import BaseCommand, BaseCommandHandler
from app.logic.exceptions.chat import ChatNotFound


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    chat_oid: str
    text: str


@dataclass(frozen=True)
class CreateMessageBaseCommandHandler(BaseCommandHandler):
    message_repository: BaseMessageRepository
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        chat_oid = command.chat_oid
        
        chat = await self.chat_repository.get_chat_by_oid(chat_oid)
        if not chat:
            raise ChatNotFound(chat_oid)

        message = Message(text=Text(command.text))
        await self.message_repository.add_message(chat_oid, message)
        chat.add_message(message)

        return message
