from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Debug
    DEBUG: bool

    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_NAME: str
    DB_USER: str

    @cached_property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()