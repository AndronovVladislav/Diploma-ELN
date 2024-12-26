from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped

from db import Base, NonUpdatableNow


class Role(Enum):
    ADMIN = 'AD'
    ANALYST = 'AN'
    SCIENTIST = 'SC'


class User(Base):
    name: Mapped[str]
    surname: Mapped[str]
    hashed_password: Mapped[str]
    registered_at: Mapped[NonUpdatableNow]
    role: Mapped[Role]

    session_expires_at: Mapped[datetime]
