import os
from pathlib import Path
from typing import Annotated, cast

from pydantic import Field, computed_field
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file() -> str:
    match os.getenv('ENV_TYPE'):
        case 'stable':
            return '.stable.env'
        case _:
            return '.env'


BASE_DIR = Path(__file__).parent
ENV_FILE = BASE_DIR / 'env' / get_env_file()


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding='utf-8', extra='ignore')


class DBSettings(ConfigBase):
    host: str
    port: int
    user: str
    password: SecretStr
    name: Annotated[str, "Name of database"]

    @computed_field
    def url(self) -> str:
        prefix = 'postgresql+asyncpg'
        return f'{prefix}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'

    @computed_field
    def migrations_url(self) -> str:
        prefix = 'postgresql+psycopg2'
        return f'{prefix}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'

    model_config = SettingsConfigDict(env_prefix='db_')


class AuthJWTSettings(ConfigBase):
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_prefix='jwt_')


class Settings(ConfigBase):
    DEBUG: bool
    db: DBSettings = Field(default_factory=DBSettings)
    jwt: AuthJWTSettings = Field(default_factory=AuthJWTSettings)


settings = Settings()
