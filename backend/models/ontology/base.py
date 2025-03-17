from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator

from neo4j import AsyncGraphDatabase, AsyncSession

from backend.config import settings

type Neo4jValue = str | int | float | bool
type Neo4jList = Annotated[list[Neo4jValue], 'Homogeneous plain list']


class Neo4jHelper:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def close(self):
        if self.driver is not None:
            await self.driver.close()

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.driver.session(database=settings.neo4j.db) as session:
            try:
                yield session
            except Exception as e:
                # TODO: поменять на logging
                print(f'Query failed: {e}')
            finally:
                if session is not None:
                    await session.close()


db_helper = Neo4jHelper(
    uri=settings.neo4j.uri,
    user=settings.neo4j.user,
    password=settings.neo4j.password.get_secret_value(),
)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with db_helper.get_session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper
