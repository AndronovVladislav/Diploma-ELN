from enum import StrEnum

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column

from backend.models.base import Base, NonUpdatableNow, UpdatableNow


class ExperimentKind(StrEnum):
    LABORATORY = 'laboratory'
    COMPUTATIONAL = 'computational'


class SchemaKind(StrEnum):
    INPUT = 'input'
    OUTPUT = 'output'
    PARAMETERS = 'parameters'
    CONTEXT = 'context'


class Experiment(Base):
    """
    Базовые поля, общие для всех экспериментов.
    """
    __abstract__ = True

    experiment_type: Mapped[ExperimentKind]
    name: Mapped[str]
    description: Mapped[str]

    created_at: Mapped[NonUpdatableNow]
    updated_at: Mapped[UpdatableNow]


class Measurement(Base):
    """
    Хранит строки таблицы измерений для лабораторного эксперимента.
    """
    row_id: Mapped[int]
    column_id: Mapped[int]
    value: Mapped[str]  # TODO: возможно такой тип будет проблемой, но пока он такой не забывать парсить в порядке [(float | bool), str]


class LaboratoryExperiment(Experiment):
    measurements: Mapped[list[Measurement]] = relationship(Measurement)


class Schema(Base):
    type: Mapped[SchemaKind]
    data: Mapped[dict] = mapped_column(JSONB)


class ComputationalExperimentData(Base):
    input: Mapped[Schema] = relationship(Schema)
    output: Mapped[Schema] = relationship(Schema)
    parameters: Mapped[Schema] = relationship(Schema)
    context: Mapped[Schema] = relationship(Schema)


class ComputationalExperimentTemplate(Base):
    input_schema = relationship(Schema)
    output_schema = relationship(Schema)
    parameters_schema = relationship(Schema)
    context_schema = relationship(Schema)


class ComputationalExperiment(Experiment):
    template: Mapped['ComputationalExperimentTemplate'] = relationship(ComputationalExperimentTemplate)
    data: Mapped['ComputationalExperimentData'] = relationship(ComputationalExperimentData, backref='computational_experiment')
