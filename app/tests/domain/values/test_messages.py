from datetime import datetime

import pytest

from app.domain.entities.messages import Message
from app.domain.exceptions.messages import TextTooLongException
from app.domain.values.messages import Text


class TestMessages:

    def test_create_success(self):
        text = Text('hello world')
        message = Message(text=text)

        assert message.text == text
        assert message.created_at.date() == datetime.today().date()

    def test_create_text_too_long(self):
        with pytest.raises(TextTooLongException):
            Text('a' * 256)
