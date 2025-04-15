from typing import Any

import polars as pl
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import inspect

from backend.base import ONTOLOGIES_MAPPING
from backend.models.experiment import Column, Measurement, LaboratoryExperiment
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ColumnDetails


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


def check_ontologies(columns: list[dict]) -> None:
    for col in columns:
        if col['ontology'] not in ONTOLOGIES_MAPPING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Указана несуществующая онтология "{col['ontology']}" для столбца "{col['name']}"',
            )


def construct_lab_experiment(experiment: LaboratoryExperiment) -> LaboratoryExperimentDetails:
    table = pivot_measurements(experiment.measurements, experiment.columns)

    result = LaboratoryExperimentDetails(
        name=experiment.info.name,
        description=experiment.info.description,
        measurements=table,
        columns=[
            ColumnDetails(id=i, name=col.name, ontology=col.ontology, ontology_ref=col.ontology_ref)
            for i, col in enumerate(experiment.columns)
        ],
    )

    return result
