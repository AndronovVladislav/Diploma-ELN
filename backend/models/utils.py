from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.config import settings


class DatabaseHelper:
    def __init__(self,
                 url: str,
                 echo: bool,
                 echo_pool: bool,
                 pool_size: int,
                 max_overflow: int,
                 ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()


db_helper = DatabaseHelper(
    url=settings.db.url.get_secret_value(),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)


def connection(method):
    """
    Декоратор, создающий SQLAlchemy-сессию, если она не передана через kwargs.

    :param method: async Callable-объект, имеющий среди параметров session: AsyncSession
    :return:
    """
    async def wrapper(*args, **kwargs):
        session = kwargs.pop('session', None) or db_helper.session_factory()
        try:
            result = await method(*args, session=session, **kwargs)
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    return wrapper
