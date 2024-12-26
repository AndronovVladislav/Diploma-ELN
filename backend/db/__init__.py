import datetime
from functools import partial
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped

from config import settings

# from models.users import User  # noqa

Id = Annotated[int, mapped_column(primary_key=True)]
NonUpdatableNow = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())")),
]
UpdatableNow = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=partial(datetime.datetime.now, tz=datetime.UTC),
    ),
]


class Base(DeclarativeBase):
    id: Mapped[Id]

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """
        Relationships не используются в repr(), т.к. могут вести к неожиданным
        подгрузкам
        """
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or i < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"



engine = create_async_engine(
    settings.db.url,
    echo=settings.DEBUG,
    # expire_on_commit=False,
)
async_session_factory = async_sessionmaker(engine)


async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
