from app.domain.entities.chat import Chat
from app.domain.entities.messages import Message


def convert_message_to_document(message: Message) -> dict:
    return {
        'oid': message.oid,
        'text': message.text.as_genetic_type(),
        'created_at': message.created_at
    }


def convert_chat_entity_to_document(chat: Chat) -> dict:
    return {
        'oid': chat.oid,
        'title': chat.title.as_genetic_type(),
        'created_at': chat.created_at,
        'messages': [convert_message_to_document(message) for message in chat.messages]
    }
