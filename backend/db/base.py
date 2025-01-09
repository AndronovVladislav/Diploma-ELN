import datetime
from functools import partial
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

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
        Relationships не используются в repr(), так как могут вести к дополнительным неожиданным запросам.
        """
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or i < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'
