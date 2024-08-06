from datetime import datetime
from uuid import uuid4

import pytest
from faker import Faker

from app.domain.entities.messages import Message
from app.domain.exceptions.messages import TextTooLongException
from app.domain.values.messages import Text


class TestMessages:

    def test_create_success(self, faker: Faker):
        text = Text(faker.text(max_nb_chars=20))
        message = Message(text=text, chat_oid=str(uuid4))

        assert message.text == text
        assert message.created_at.date() == datetime.today().date()

    def test_create_text_too_long(self):
        with pytest.raises(TextTooLongException):
            Text('a' * 256)
