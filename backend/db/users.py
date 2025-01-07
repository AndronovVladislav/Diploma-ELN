from enum import StrEnum

from sqlalchemy.orm import Mapped

from db.base import Base, NonUpdatableNow


class Role(StrEnum):
    ADMIN = 'admin'
    ANALYST = 'analyst'
    SCIENTIST = 'scientist'


class User(Base):
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    hashed_password: Mapped[str]
    registered_at: Mapped[NonUpdatableNow]
    role: Mapped[Role]
