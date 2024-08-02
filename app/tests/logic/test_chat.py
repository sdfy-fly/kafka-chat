import pytest

from app.domain.entities.chat import Chat
from app.domain.events.chat import NewChatCreated
from app.infra.repositories.chat import BaseChatRepository
from app.logic.commands.chat import CreateChatCommand
from app.logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository: BaseChatRepository,
        mediator: Mediator
):
    chat_title = 'new chat'
    command = CreateChatCommand(chat_title)
    chat: list = await mediator.handle_command(command)
    chat: Chat = chat[0]

    assert isinstance(chat, Chat)
    assert chat.title.as_genetic_type() == chat_title
    assert chat_repository.is_chat_exists(chat_title)

    events = chat.pull_events()
    event = events[0]
    assert isinstance(event, NewChatCreated)
