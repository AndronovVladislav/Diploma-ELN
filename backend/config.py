import os
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file() -> str:
    match os.getenv('ENV_TYPE'):
        case 'stable':
            return '.stable.env'
        case _:
            return '.env'


BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / 'env' / get_env_file()


class DBSettings(BaseModel):
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_NAME: str
    DB_USER: str

    @cached_property
    def DATABASE_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7


class Settings(BaseSettings):
    DEBUG: bool
    db = DBSettings()
    jwt = AuthJWTSettings()

    model_config = SettingsConfigDict(env_file=ENV_FILE)

settings = Settings()
