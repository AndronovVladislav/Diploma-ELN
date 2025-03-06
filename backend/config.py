import os
from functools import cached_property
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
    host: str
    port: int
    workers: int
    timeout: int
    reload: bool

    model_config = SettingsConfigDict(env_prefix='uvi_')


class PostgresSettings(ConfigBase):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    @computed_field
    def url(self) -> str:
        prefix = 'postgresql+asyncpg'
        return f'{prefix}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}'

    model_config = SettingsConfigDict(env_prefix='pg_')

class Neo4jSettings(ConfigBase):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    model_config = SettingsConfigDict(env_prefix='neo4j_')

    @cached_property
    def uri(self) -> str:
        return f'neo4j://{self.host}:{self.port}'


class AuthJWTSettings(ConfigBase):
    algorithm: str
    access_token_expire_minutes: int
    private_key_path: Path
    public_key_path: Path
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(env_prefix='jwt_')


class Settings(ConfigBase):
    db: PostgresSettings = Field(default_factory=PostgresSettings)
    jwt: AuthJWTSettings = Field(default_factory=AuthJWTSettings)
    neo4j: Neo4jSettings = Field(default_factory=Neo4jSettings)
    uvicorn: UvicornSettings = Field(default_factory=UvicornSettings)


settings = Settings()
