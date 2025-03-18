from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, relationship, mapped_column, declared_attr

from backend.models.base import Base, NonUpdatableNow, UpdatableNow, Id


class Experiment(Base):
    """
    Базовые поля, общие для всех экспериментов.
    """
    __abstract__ = True

    user_id: Mapped[Id] = mapped_column(ForeignKey('users.id'))

    path: Mapped[str]
    description: Mapped[str]
    created_at: Mapped[NonUpdatableNow]
    updated_at: Mapped[UpdatableNow]


class Measurement(Base):
    """
    Хранит строки таблицы измерений для лабораторного эксперимента.
    """
    row: Mapped[int]
    column: Mapped[int]
    value: Mapped[
        str]  # TODO: возможно такой тип будет проблемой, но пока он такой не забывать парсить в порядке [(float | bool), str]

    experiment_id: Mapped[Id] = mapped_column(ForeignKey('laboratory_experiments.id'))


class Ontology(Base):
    __tablename__ = 'ontologies'

    name: Mapped[str]
    label: Mapped[str]


class ColumnDescription(Base):
    name: Mapped[str]
    ontology_element: Mapped[str]

    ontology_id: Mapped[Id] = mapped_column(ForeignKey('ontologies.id'))
    ontology: Mapped['Ontology'] =  relationship('Ontology')

    experiment_id: Mapped[Id] = mapped_column(ForeignKey('laboratory_experiments.id'))


class LaboratoryExperiment(Experiment):
    user: Mapped['User'] = relationship(back_populates='lab_experiments')

    measurements: Mapped[list['Measurement']] = relationship()
    columns: Mapped[list['ColumnDescription']] = relationship()


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

    input_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id'))
    output_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id'))
    parameters_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id'))
    context_id: Mapped[Id] = mapped_column(ForeignKey('schemas.id'))

    @classmethod
    @declared_attr
    def input(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.input_id])

    @classmethod
    @declared_attr
    def output(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.output_id])

    @classmethod
    @declared_attr
    def parameters(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.parameters_id])

    @classmethod
    @declared_attr
    def context(cls) -> Mapped[Schema]:
        return relationship('Schema', foreign_keys=[cls.context_id])


class ComputationalExperimentTemplate(SchemaLinkedTable):
    experiments: Mapped[list['ComputationalExperiment']] = relationship(back_populates='template')


class ComputationalExperimentData(SchemaLinkedTable):
    experiment_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiments.id'))
    experiment: Mapped['ComputationalExperiment'] = relationship(back_populates='data')


class ComputationalExperiment(Experiment):
    template_id: Mapped[Id] = mapped_column(ForeignKey('computational_experiment_templates.id'))

    template: Mapped['ComputationalExperimentTemplate'] = relationship(back_populates='experiments')
    data: Mapped[list['ComputationalExperimentData']] = relationship(back_populates='experiment')
    user: Mapped['User'] = relationship(back_populates='computational_experiments')
