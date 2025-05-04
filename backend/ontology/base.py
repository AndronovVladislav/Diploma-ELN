from contextlib import asynccontextmanager
from typing import Annotated, AsyncIterator, Self

from fastapi import HTTPException
from neo4j import AsyncGraphDatabase, AsyncSession

from backend.base import CypherRelatedError
from backend.config import settings


class ExactlyOneReturnClauseException(CypherRelatedError):
    message = 'Cypher query must have exactly one return clause'


class CypherCondition:
    def __init__(self, expression: str) -> None:
        self.expression = expression

    def __and__(self, other: Self) -> Self:
        return CypherCondition(f'({self.expression} AND {other.expression})')

    def __or__(self, other: Self) -> Self:
        return CypherCondition(f'({self.expression} OR {other.expression})')

    def __invert__(self) -> Self:
        return CypherCondition(f'(NOT {self.expression})')

    def __str__(self) -> str:
        return self.expression


class CypherQueryBuilder:
    def __init__(self) -> None:
        self._match_clauses: list[str] = []
        self._where_clause: CypherCondition | None = None
        self._return_clause: str | None = None
        self._limit_clause: int | None = None

    def match(self, pattern: str) -> Self:
        self._match_clauses.append(pattern)
        return self

    def where(self, condition: CypherCondition) -> Self:
        if self._where_clause is None:
            self._where_clause = condition
        else:
            self._where_clause &= condition
        return self

    def return_(self, return_expr: str) -> Self:
        if self._return_clause is None:
            self._return_clause = return_expr
            return self
        else:
            raise ExactlyOneReturnClauseException

    def limit(self, n: int) -> Self:
        self._limit_clause = n
        return self

    def clear(self) -> None:
        self._match_clauses = []
        self._where_clause = None
        self._return_clause = None
        self._limit_clause = None

    def build(self) -> str:
        query_parts: list[str] = []

        if self._match_clauses:
            match_str = 'MATCH ' + ', '.join(self._match_clauses)
            query_parts.append(match_str)

        if self._where_clause:
            where_str = 'WHERE ' + str(self._where_clause)
            query_parts.append(where_str)

        if self._return_clause:
            return_str = 'RETURN ' + self._return_clause
            query_parts.append(return_str)
        else:
            raise ExactlyOneReturnClauseException

        if self._limit_clause is not None:
            query_parts.append(f'LIMIT {self._limit_clause}')

        self.clear()
        return '\n'.join(query_parts)


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
            yield session


db_helper = Neo4jHelper(
    uri=settings.neo4j.uri,
    user=settings.neo4j.user,
    password=settings.neo4j.password.get_secret_value(),
)
builder = CypherQueryBuilder()


def connection(method):
    async def wrapper(*args, **kwargs):
        async with db_helper.get_session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                print(f'Query failed: {e}')
                raise e
            finally:
                await session.close()

    return wrapper


@connection
async def validate_all_ontology_uris_exist(uris: set[str], session: AsyncSession) -> None:
    q = (
        builder
        .match('(n)')
        .where(CypherCondition('n.uri IN $uris'))
        .return_('n.uri AS uri')
        .build()
    )
    result = await session.run(q, {'uris': list(uris)})
    found_uris = {row['uri'] async for row in result}
    missing = uris - found_uris
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f'Следующие URI не найдены в онтологиях: {sorted(missing)}'
        )
