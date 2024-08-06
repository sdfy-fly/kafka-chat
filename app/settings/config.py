from pydantic import Field
from pydantic_settings import BaseSettings


class MongoChatSettings(BaseSettings):
    database: str = Field(alias='MONGO_CHAT_DATABASE', default='chat')
    chat_collection: str = Field(alias='MONGO_CHAT_COLLECTION', default='chat')
    message_collection: str = Field(alias='MONGO_MESSAGE_COLLECTION', default='message')


class MongoSettings(BaseSettings):
    host: str = Field(alias='MONGO_HOST', default='localhost')
    port: int = Field(alias='MONGO_PORT', default='27017')
    chat: MongoChatSettings = MongoChatSettings()

    @property
    def connection_uri(self):
        return f'mongodb://{self.host}:{self.port}'


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()


settings = Settings()
