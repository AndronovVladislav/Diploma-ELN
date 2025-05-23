from enum import StrEnum

from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr

from backend.common.enums import ExperimentKind
from backend.models.base import Base, NonUpdatableNow, UpdatableNow, Id


class PathMixin:
    path: Mapped[str]

    @property
    def name(self) -> str:
        return self.path.rsplit('/', 1)[-1]

    @name.setter
    def name(self, new_name: str) -> None:
        self.path = '/'.join((self.path.split('/')[:-1], new_name))


class OwnableMixin:
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))


class Experiment(OwnableMixin, PathMixin, Base):
    """
    Базовые поля, общие для всех экспериментов.
    """

    description: Mapped[str]
    kind: Mapped[ExperimentKind] = mapped_column()

    created_at: Mapped[NonUpdatableNow]
    updated_at: Mapped[UpdatableNow]

    __mapper_args__ = {
        'polymorphic_on': kind,
        'polymorphic_identity': 'base'
    }


class Column(Base):
    name: Mapped[str]
    ontology: Mapped[str]
    ontology_ref: Mapped[str]
    is_main: Mapped[bool] = mapped_column(default=False, server_default=text('false'))

    experiment_id: Mapped[int] = mapped_column(ForeignKey('laboratory_experiments.id', ondelete='CASCADE'))


class Measurement(Base):
    """
    Хранит строки таблицы измерений для лабораторного эксперимента.
    """
    row: Mapped[int]
    column: Mapped[int] = mapped_column(ForeignKey('columns.id', ondelete='CASCADE'))
    value: Mapped[str]

    experiment_id: Mapped[int] = mapped_column(ForeignKey('laboratory_experiments.id', ondelete='CASCADE'))


class LaboratoryExperiment(Experiment):
    id: Mapped[Id] = mapped_column(ForeignKey('experiments.id', ondelete='CASCADE'))

    measurements: Mapped[list['Measurement']] = relationship(cascade='all, delete-orphan', passive_deletes=True)
    columns: Mapped[list['Column']] = relationship(cascade='all, delete-orphan', passive_deletes=True)

    __mapper_args__ = {
        'polymorphic_identity': ExperimentKind.LABORATORY
    }


class SchemaKind(StrEnum):
    INPUT = 'input'
    OUTPUT = 'output'
    PARAMETERS = 'parameters'
    CONTEXT = 'context'


class Schema(Base):
    type: Mapped['SchemaKind']
    data: Mapped[dict] = mapped_column(JSONB)


class SchemaLinkedTableMixin:
    input_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id', ondelete='RESTRICT'))
    output_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id', ondelete='RESTRICT'))
    parameters_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id', ondelete='RESTRICT'))
    context_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id', ondelete='RESTRICT'))

    @declared_attr
    @classmethod
    def input(cls) -> Mapped['Schema']:
        return relationship('Schema', foreign_keys=[cls.input_id])

    @declared_attr
    @classmethod
    def output(cls) -> Mapped['Schema']:
        return relationship('Schema', foreign_keys=[cls.output_id])

    @declared_attr
    @classmethod
    def parameters(cls) -> Mapped['Schema']:
        return relationship('Schema', foreign_keys=[cls.parameters_id])

    @declared_attr
    @classmethod
    def context(cls) -> Mapped['Schema']:
        return relationship('Schema', foreign_keys=[cls.context_id])


class ComputationalExperimentTemplate(OwnableMixin, SchemaLinkedTableMixin, PathMixin, Base):
    experiments: Mapped[list['ComputationalExperiment']] = relationship(back_populates='template')


class ComputationalExperimentData(SchemaLinkedTableMixin, Base):
    row: Mapped[int]
    experiment_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiments.id', ondelete='CASCADE'))
    experiment: Mapped['ComputationalExperiment'] = relationship(back_populates='data', passive_deletes=True)


class ComputationalExperiment(Experiment):
    id: Mapped[Id] = mapped_column(ForeignKey('experiments.id', ondelete='CASCADE'))

    template_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiment_templates.id',
                                                       ondelete='RESTRICT'),
                                            )

    template: Mapped['ComputationalExperimentTemplate'] = relationship(back_populates='experiments')
    data: Mapped[list['ComputationalExperimentData']] = relationship(back_populates='experiment',
                                                                     cascade='all, delete-orphan',
                                                                     )

    __mapper_args__ = {
        'polymorphic_identity': ExperimentKind.COMPUTATIONAL
    }
