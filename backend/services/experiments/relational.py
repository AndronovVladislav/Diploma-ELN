from enum import StrEnum

import polars as pl
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import User
from backend.models.experiment import LaboratoryExperiment, ColumnDescription
from backend.models.utils import connection
from backend.schemas.experiments import LaboratoryExperiment as LaboratoryExperimentSchema, \
    ColumnDescription as ColumnDescriptionSchema


class ExperimentKind(StrEnum):
    LABORATORY = 'Лабораторный'
    COMPUTATIONAL = 'Вычислительный'


def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


class Column(BaseModel):
    row: int
    column: int
    value: str


def enhanced_obj_to_dict(obj):
    data = to_dict(obj)
    inspect_manager = inspect(obj.__class__)
    relationships = inspect_manager.relationships

    for rel in relationships:
        value = getattr(obj, rel.key)
        data[rel.key] = to_dict(value) if value else None

        if isinstance(value, list):
            data[rel.key] = [to_dict(child) for child in value]
        else:
            data[rel.key] = None
    return data


@connection
async def get_user_experiments(username: str, session: AsyncSession) -> ...:
    q = (
        select(User)
        .options(selectinload(User.lab_experiments), selectinload(User.computational_experiments))
        .filter_by(username=username)
    )
    user = (await session.execute(q)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь с таким id не найден')

    result = []

    for exp in user.experiments:
        exp_dict = to_dict(exp)
        exp_dict['kind'] = ExperimentKind.LABORATORY if exp in user.lab_experiments else ExperimentKind.COMPUTATIONAL
        result.append(exp_dict)

    return result


@connection
async def get_lab_experiment_data(experiment_id: int, session: AsyncSession) -> ...:
    q = (
        select(LaboratoryExperiment)
        .options(
            selectinload(LaboratoryExperiment.measurements),
            selectinload(LaboratoryExperiment.columns).selectinload(ColumnDescription.ontology),
        )
        .filter_by(id=experiment_id)
    )
    experiment = (await session.execute(q)).scalar_one_or_none()

    mapping = {}
    for column in experiment.columns:
        for measurement in experiment.measurements:
            if measurement.column == column.id:
                mapping[str(measurement.column)] = column.name

    table = pl.DataFrame(
        [Column(row=record.row, column=record.column, value=record.value)
         for record in experiment.measurements]
    ).pivot('column', index='row', values='value').rename(mapping)

    result = LaboratoryExperimentSchema(
        name=experiment.path.rsplit('/', 1)[-1],
        description=experiment.description,
        data=table.to_dicts(),
        columns=[
            ColumnDescriptionSchema(name=col.name, ontology=col.ontology.name, ontology_element=col.ontology_element)
            for col in experiment.columns
        ],
    )

    return result
