from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.common.enums import Role
from backend.models.base import Base, NonUpdatableNow, UpdatableNow, Id

if TYPE_CHECKING:
    from backend.models.experiment import Experiment


class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Role]

    profile: Mapped['Profile'] = relationship(back_populates='user', cascade='all, delete-orphan')
    experiments: Mapped[list['Experiment']] = relationship(cascade='all, delete-orphan',
                                                           passive_deletes=True,
                                                           )


class Profile(Base):
    name: Mapped[str | None] = mapped_column(default=None)
    surname: Mapped[str | None] = mapped_column(default=None)
    registered_at: Mapped[NonUpdatableNow | None] = mapped_column(default=None)
    position: Mapped[str | None] = mapped_column(default=None)
    email: Mapped[str | None] = mapped_column(default=None)
    last_login: Mapped[UpdatableNow | None] = mapped_column(default=None)

    user_id: Mapped[Id] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='profile')
