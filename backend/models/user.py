from enum import StrEnum

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.models.base import Base, NonUpdatableNow, Id


class Role(StrEnum):
    ADMIN = 'admin'
    RESEARCHER = 'researcher'


class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str]
    role: Mapped[Role]

    profile: Mapped['Profile'] = relationship(back_populates='user')
    lab_experiments: Mapped['LaboratoryExperiment'] = relationship(back_populates='user')
    computational_experiments: Mapped['ComputationalExperiment'] = relationship(back_populates='user')

    @property
    def experiments(self) -> list['Experiment']:
        return self.lab_experiments + self.computational_experiments


class Profile(Base):
    name: Mapped[str]
    surname: Mapped[str]
    registered_at: Mapped[NonUpdatableNow]

    user_id: Mapped[Id] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='profile')
