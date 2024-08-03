from app.infra.repositories.chat import BaseChatRepository
from app.logic.commands.chat import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator


def init_mediator(
        mediator: Mediator,
        chat_repository: BaseChatRepository
):
    mediator.register_command(
        command=CreateChatCommand,
        command_handlers=[
            CreateChatCommandHandler(repository=chat_repository)
        ]
    )
