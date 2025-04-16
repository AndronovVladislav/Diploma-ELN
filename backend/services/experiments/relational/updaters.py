from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.common.enums import ExperimentKind
from backend.models.experiment import LaboratoryExperiment, Column, Measurement, Experiment
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails
from backend.schemas.experiments.requests import UpdateLaboratoryExperimentRequest
from backend.services.experiments.relational.utils import check_ontologies, construct_lab_experiment

INFORMATIONAL_ATTRIBUTES = {'data', 'description'}


@connection
async def update_experiment_data(experiment_id: int,
                                 update: UpdateLaboratoryExperimentRequest,
                                 session: AsyncSession,
                                 ) -> LaboratoryExperimentDetails | None:
    experiment = await session.get(Experiment, experiment_id)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Эксперимент с таким id не найден')

    match experiment.kind:
        case ExperimentKind.LABORATORY:
            return await update_lab_experiment_data(experiment_id, update, session=session)


async def update_lab_experiment_data(experiment_id: int,
                                     update: UpdateLaboratoryExperimentRequest,
                                     session: AsyncSession,
                                     ) -> LaboratoryExperimentDetails:
    q = (
        select(LaboratoryExperiment)
        .filter_by(id=experiment_id)
        .options(
            selectinload(LaboratoryExperiment.info),
            selectinload(LaboratoryExperiment.measurements),
            selectinload(LaboratoryExperiment.columns),
        )
    )

    experiment = (await session.execute(q)).scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Лабораторный эксперимент с таким id не найден',
                            )

    update_data = update.model_dump(exclude_unset=True)
    for attr in INFORMATIONAL_ATTRIBUTES:
        if attr in update_data:
            setattr(experiment.info, attr, update_data[attr])

    if 'columns' in update_data:
        await update_columns(experiment, update_data['columns'], session=session)

    if 'measurements' in update_data:
        update_measurements(experiment, update_data['measurements'])

    return construct_lab_experiment(experiment)


async def update_columns(experiment: LaboratoryExperiment, columns: list[dict], session: AsyncSession) -> None:
    current_columns = {col.name: col for col in experiment.columns}
    incoming_names = {col['name'] for col in columns}

    experiment.columns[:] = [col for col in experiment.columns if col.name in incoming_names]

    check_ontologies(columns)
    for col_data in columns:
        existing = current_columns.get(col_data['name'])

        if existing:
            existing.ontology_ref = col_data['ontology_ref']
            existing.ontology = col_data['ontology']
            existing.is_main = col_data['is_main']
        else:
            experiment.columns.append(Column(
                name=col_data['name'],
                ontology_ref=col_data['ontology_ref'],
                ontology=col_data['ontology'],
                experiment_id=experiment.id,
                is_main=col_data['is_main'],
            ))

    await session.flush()


def update_measurements(experiment: LaboratoryExperiment, measurements: list[dict[str, str | int]]) -> None:
    name_to_col = {col.name: col.id for col in experiment.columns}

    existing_measurements = {
        (measurement.row, measurement.column): measurement
        for measurement in experiment.measurements
    }

    incoming_measurements = {
        (row['row'], name_to_col[column]): value
        for row in measurements for column, value in row.items()
        if column != 'row' and column in name_to_col
    }

    experiment.measurements[:] = [
        measurement for key, measurement in existing_measurements.items()
        if key in incoming_measurements and measurement.value == incoming_measurements[key]
    ]

    for (row, col), value in incoming_measurements.items():
        if (row, col) not in existing_measurements or existing_measurements[(row, col)].value != value:
            experiment.measurements.append(Measurement(row=row, column=col, value=value))
