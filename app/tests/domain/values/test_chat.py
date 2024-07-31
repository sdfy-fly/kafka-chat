from datetime import datetime

import pytest

from app.domain.entities.chat import Chat
from app.domain.entities.messages import Message
from app.domain.events.messages import NewMessageReceivedEvent
from app.domain.exceptions.chat import TitleTooLongException
from app.domain.values.chat import Title
from app.domain.values.messages import Text


class TestChat:

    def test_create_success(self):
        title = Title('hello world')
        chat = Chat(title=title)

        assert chat.title == title
        assert not chat.messages
        assert chat.created_at.date() == datetime.today().date()

    def test_create_title_too_long(self):
        with pytest.raises(TitleTooLongException):
            Title('a' * 256)

    def test_add_message(self):
        text = Text('hello world')
        message = Message(text=text)

        title = Title('hello world')
        chat = Chat(title=title)

        chat.add_message(message)

        assert message in chat.messages

    def test_new_message_event(self):
        text = Text('hello world')
        message = Message(text=text)

        title = Title('hello world')
        chat = Chat(title=title)

        chat.add_message(message)
        events = chat.pull_events()
        pulled_events = chat.pull_events()

        assert not pulled_events, pulled_events
        assert len(events) == 1, events

        event = events[0]
        assert isinstance(event, NewMessageReceivedEvent)
        assert event.message_oid == message.oid
        assert event.message_text == message.text.as_genetic_type()
        assert event.chat_oid == chat.oid
