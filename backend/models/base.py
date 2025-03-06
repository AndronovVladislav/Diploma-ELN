import datetime
import re
from functools import partial
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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
    __abstract__ = True

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

    def __init_subclass__(cls, **kwargs):
        if '__tablename__' not in cls.__dict__:
            cls.__tablename__ = f"{re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()}s"
        super().__init_subclass__(**kwargs)
