from enum import StrEnum
from typing import Any

import polars as pl
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import inspect

from backend.base import ONTOLOGIES_MAPPING
from backend.models.experiment import Column, Measurement, LaboratoryExperiment, ComputationalExperiment, SchemaKind
from backend.ontology.base import validate_all_ontology_uris_exist
from backend.schemas.experiments.data import (
    LaboratoryExperimentDetails,
    ColumnDetails,
    ComputationalExperimentDetails,
    ComputationalExperimentRow, ComputationalExperimentTemplate,
)


class ExportType(StrEnum):
    JSON = 'json'
    XML = 'xml'


class Cell(BaseModel):
    row: int
    column: int
    value: str


def to_dict(obj) -> dict[str, Any]:
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def pivot_measurements(measurements: list[Measurement], columns: list[Column]) -> list[dict[str, str]]:
    mapping = {}
    for column in columns:
        for measurement in measurements:
            if measurement.column == column.id:
                mapping[str(measurement.column)] = column.name

    table = []
    if measurements:
        table = pl.DataFrame(
            [Cell(row=record.row, column=record.column, value=record.value)
             for record in measurements]
        ).pivot('column', index='row', values='value').rename(mapping).to_dicts()

    return table


async def check_ontologies(columns: list[dict]) -> None:
    for col in columns:
        if col['ontology'] not in ONTOLOGIES_MAPPING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Указана несуществующая онтология "{col['ontology']}" для столбца "{col['name']}"',
            )
    await validate_all_ontology_uris_exist({col['ontology_ref'] for col in columns})


def validate_schema(data: dict, schema: dict, kind: SchemaKind) -> None:
    if set(data.keys()) != set(schema.keys()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'{kind} data keys do not match template schema: expected {set(schema.keys())}, got {set(data.keys())}'
        )


def construct_lab_experiment_details(experiment: LaboratoryExperiment) -> LaboratoryExperimentDetails:
    table = pivot_measurements(experiment.measurements, experiment.columns)

    result = LaboratoryExperimentDetails(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        measurements=table,
        columns=[
            ColumnDetails(
                id=col.id,
                name=col.name,
                ontology=col.ontology,
                ontology_ref=col.ontology_ref,
                is_main=col.is_main,
            )
            for col in experiment.columns
        ],
    )

    result.columns.sort(key=lambda c: c.id)
    return result


def construct_comp_experiment_details(experiment: ComputationalExperiment) -> ComputationalExperimentDetails:
    data = [
        ComputationalExperimentRow(
            row=row.row,
            input=row.input.data,
            output=row.output.data,
            parameters=row.parameters.data,
            context=row.context.data,
        ) for row in experiment.data
    ]
    result = ComputationalExperimentDetails(
        id=experiment.id,
        template=ComputationalExperimentTemplate(
            input=experiment.template.input.data,
            output=experiment.template.output.data,
            parameters=experiment.template.parameters.data,
            context=experiment.template.context.data,
        ),
        name=experiment.name,
        description=experiment.description,
        data=data,
    )

    return result
