import os
from pathlib import Path

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


class UvicornSettings(ConfigBase):
    host: str = '0.0.0.0'
    port: int = 8000
    workers: int = 1
    timeout: int = 900

    model_config = SettingsConfigDict(env_prefix='uvi_')


class PostgresSettings(ConfigBase):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str
    echo: bool = True
    echo_pool: bool = True
    pool_size: int = 5
    max_overflow: int = 10

    @computed_field
    def url(self) -> str:
        prefix = 'postgresql+asyncpg'
        return f'{prefix}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}'

    model_config = SettingsConfigDict(env_prefix='pg_')


class AuthJWTSettings(ConfigBase):
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_prefix='jwt_')


class Settings(ConfigBase):
    db: PostgresSettings = Field(default_factory=PostgresSettings)
    jwt: AuthJWTSettings = Field(default_factory=AuthJWTSettings)
    uvicorn: UvicornSettings = Field(default_factory=UvicornSettings)


settings = Settings()
