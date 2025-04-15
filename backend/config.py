import os
import tomllib
from functools import cached_property
from pathlib import Path
from typing import Self

from pydantic import computed_field, BaseModel, ConfigDict
from pydantic.types import SecretStr
from pydantic.v1.utils import deep_update
from pydantic_settings import BaseSettings

CONFIGS_DIR = Path(__file__).parent / 'config'


def get_config_file() -> Path:
    filename = 'config'
    match os.getenv('ENV_TYPE'):
        case 'stable':
            filename += '.stable'
        case 'testing':
            filename += '.testing'
        case _:
            filename += '.dev'

    return CONFIGS_DIR / f'{filename}.toml'


CONFIG_TEMPLATE = CONFIGS_DIR / 'config.template.toml'
CONFIG_FILES = (CONFIG_TEMPLATE, get_config_file())


class UvicornSettings(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int
    debug: bool


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    database: str

    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

    dbms: str
    driver: str

    @computed_field
    def url(self) -> SecretStr:
        prefix = f'{self.dbms}+{self.driver}'
        return SecretStr(
            f'{prefix}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.database}'
        )


class Neo4jSettings(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    db: str

    @cached_property
    def uri(self) -> str:
        return f'neo4j://{self.host}:{self.port}'


class AuthJWTSettings(BaseModel):
    algorithm: str
    access_token_expire_minutes: int
    private_key_path: Path
    public_key_path: Path
    refresh_token_expire_minutes: int


class OntologiesSettings(BaseModel):
    model_config = ConfigDict(extra='allow')


class Settings(BaseSettings):
    uvicorn: UvicornSettings
    db: DatabaseSettings
    neo4j: Neo4jSettings
    jwt: AuthJWTSettings
    ontologies: OntologiesSettings

    @classmethod
    def load(cls) -> Self:
        config_data: dict = {}
        for path in CONFIG_FILES:
            with open(path, 'rb') as f:
                config_data = deep_update(config_data, tomllib.load(f))
        return cls(**config_data)


settings = Settings.load()
