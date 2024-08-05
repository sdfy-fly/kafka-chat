from pydantic import Field
from pydantic_settings import BaseSettings


class MongoSettings(BaseSettings):
    host: str = Field(alias='MONGO_HOST', default='localhost')
    port: int = Field(alias='MONGO_PORT', default='27017')

    @property
    def connection_uri(self):
        return f'mongodb://{self.host}:{self.port}'


class Settings(BaseSettings):
    mongo: MongoSettings = MongoSettings()


settings = Settings()
