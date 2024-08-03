import pytest
from faker import Faker

from app.domain.entities.chat import Chat
from app.domain.events.chat import NewChatCreated
from app.domain.values.chat import Title
from app.infra.repositories.chat import BaseChatRepository
from app.logic.commands.chat import CreateChatCommand
from app.logic.exceptions.messages import ChatAlreadyExists
from app.logic.mediator import Mediator


class TestChat:

    @pytest.mark.asyncio
    async def test_create_command_success(
            self,
            chat_repository: BaseChatRepository,
            mediator: Mediator,
            faker: Faker
    ):
        chat_title = faker.sentence()
        command = CreateChatCommand(title=chat_title)
        chats: list = await mediator.handle_command(command)
        chat: Chat = chats[0]

        assert isinstance(chat, Chat)
        assert chat.title.as_genetic_type() == chat_title
        assert await chat_repository.is_chat_exists(chat_title)

        events = chat.pull_events()
        event = events[0]
        assert isinstance(event, NewChatCreated)

    @pytest.mark.asyncio
    async def test_create_command_title_already_exists(
            self,
            chat_repository: BaseChatRepository,
            mediator: Mediator,
            faker: Faker
    ):
        chat_title = faker.sentence()
        
        chat = Chat(title=Title(chat_title))
        await chat_repository.add_chat(chat)

        with pytest.raises(ChatAlreadyExists):
            command = CreateChatCommand(title=chat_title)
            await mediator.handle_command(command)

        assert len(chat_repository._saved_chats) == 1
