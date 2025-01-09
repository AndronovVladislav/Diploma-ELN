from typing import Annotated, AsyncGenerator

from neo4j import AsyncGraphDatabase, AsyncSession

from config import settings

type Neo4jValue = str | int | float | bool
type Neo4jList = Annotated[list['Neo4jValue'], 'Homogeneous plain list']


class Neo4jHelper:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async def close(self):
        if self.driver is not None:
            await self.driver.close()

    async def get_session(self, db: str) -> AsyncGenerator[AsyncSession, None]:
        async with self.driver.session(database=db) as session:
            try:
                yield session
            except Exception as e:
                # TODO: поменять на logging
                print(f'Query failed: {e}') 
            finally:
                if session is not None:
                    await session.close()


neo4j_helper = Neo4jHelper(
    url=settings.neo4j.url,
    echo=settings.neo4j.echo,
    echo_pool=settings.neo4j.echo_pool,
    pool_size=settings.neo4j.pool_size,
    max_overflow=settings.neo4j.max_overflow,
)
