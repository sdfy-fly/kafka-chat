from typing import Mapping, Any

from app.domain.entities.chat import Chat
from app.domain.entities.messages import Message
from app.domain.values.chat import Title
from app.domain.values.messages import Text


def convert_message_to_document(message: Message) -> dict:
    return {
        'oid': message.oid,
        'chat_oid': message.chat_oid,
        'text': message.text.as_genetic_type(),
        'created_at': message.created_at
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        'oid': chat.oid,
        'title': chat.title.as_genetic_type(),
        'created_at': chat.created_at,
    }


def convert_message_document_to_entity(message_document: Mapping[str, Any]) -> Message:
    return Message(
        oid=message_document['oid'],
        chat_oid=message_document['chat_oid'],
        text=Text(message_document['text']),
        created_at=message_document['created_at']
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> Chat:
    return Chat(
        oid=chat_document['oid'],
        title=Title(chat_document['title']),
        created_at=chat_document['created_at']
    )
