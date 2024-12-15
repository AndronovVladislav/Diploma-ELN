from enum import Enum

from sqlalchemy.orm import Mapped

from models import Base, Id, NonUpdatableNow


class Role(Enum):
    ADMIN = 'AD'
    ANALYST = 'AN'
    SCIENTIST = 'SC'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[Id]
    name: Mapped[str]
    surname: Mapped[str]
    hashed_password: Mapped[str]
    registrated_at: Mapped[NonUpdatableNow]
    role: Mapped[Role]
