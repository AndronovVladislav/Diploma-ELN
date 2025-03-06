from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr

from backend.models.base import Base, NonUpdatableNow, UpdatableNow, Id


class ExperimentKind(StrEnum):
    LABORATORY = 'laboratory'
    COMPUTATIONAL = 'computational'


class Experiment(Base):
    """
    Базовые поля, общие для всех экспериментов.
    """
    __abstract__ = True

    user_id: Mapped[Id] = mapped_column(ForeignKey('users.id'))

    kind: Mapped[ExperimentKind]
    name: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[NonUpdatableNow]
    updated_at: Mapped[UpdatableNow]


class Measurement(Base):
    """
    Хранит строки таблицы измерений для лабораторного эксперимента.
    """
    row: Mapped[int]
    column: Mapped[int]
    value: Mapped[str]  # TODO: возможно такой тип будет проблемой, но пока он такой не забывать парсить в порядке [(float | bool), str]

    experiment_id: Mapped[Id] = mapped_column(ForeignKey('laboratory_experiments.id'))


class LaboratoryExperiment(Experiment):
    measurements: Mapped[list['Measurement']] = relationship()


class SchemaKind(StrEnum):
    INPUT = 'input'
    OUTPUT = 'output'
    PARAMETERS = 'parameters'
    CONTEXT = 'context'


class Schema(Base):
    type: Mapped[SchemaKind]
    data: Mapped[dict] = mapped_column(JSONB)


class SchemaLinkedTable(Base):
    __abstract__ = True

    @declared_attr
    def input_schema_id(cls) -> Mapped[Id]:
        return mapped_column(ForeignKey('schemas.id'))

    @declared_attr
    def output_schema_id(cls) -> Mapped[Id]:
        return mapped_column(ForeignKey('schemas.id'))

    @declared_attr
    def parameters_schema_id(cls) -> Mapped[Id]:
        return mapped_column(ForeignKey('schemas.id'))

    @declared_attr
    def context_schema_id(cls) -> Mapped[Id]:
        return mapped_column(ForeignKey('schemas.id'))

    @declared_attr
    def input(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.input_schema_id])

    @declared_attr
    def output(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.output_schema_id])

    @declared_attr
    def parameters(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.parameters_schema_id])

    @declared_attr
    def context(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.context_schema_id])


class ComputationalExperimentTemplate(SchemaLinkedTable):
    pass


class ComputationalExperimentData(SchemaLinkedTable):
    experiment_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiments.id'))


class ComputationalExperiment(Experiment):
    template_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiment_templates.id'))

    template: Mapped['ComputationalExperimentTemplate'] = relationship(back_populates='experiments')
    data: Mapped[list['ComputationalExperimentData']] = relationship()
