from fastapi import HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import User
from backend.models.experiment import (
    LaboratoryExperiment,
    Column,
    Measurement,
    Experiment,
    ComputationalExperiment,
    ComputationalExperimentData,
    Schema,
    SchemaKind, ComputationalExperimentTemplate,
)
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ComputationalExperimentDetails
from backend.schemas.experiments.requests import UpdateLaboratoryExperimentRequest, UpdateComputationalExperimentRequest
from backend.services.experiments.relational.common import (
    EXPERIMENT_NOT_FOUND_MESSAGE,
    OTHER_EXPERIMENT_DELETING_MESSAGE,
)
from backend.services.experiments.relational.utils import check_ontologies, construct_lab_experiment_details, \
    construct_comp_experiment_details

INFORMATIONAL_ATTRIBUTES = {'description', 'path'}


@connection
async def update_lab_experiment_data(experiment_id: int,
                                     update: UpdateLaboratoryExperimentRequest,
                                     session: AsyncSession,
                                     ) -> LaboratoryExperimentDetails:
    q = (
        select(LaboratoryExperiment)
        .options(
            selectinload(LaboratoryExperiment.measurements),
            selectinload(LaboratoryExperiment.columns),
        )
        .filter_by(id=experiment_id)
    )

    experiment = (await session.execute(q)).scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EXPERIMENT_NOT_FOUND_MESSAGE)

    update_data = update.model_dump(exclude_unset=True)
    for attr in INFORMATIONAL_ATTRIBUTES:
        if attr in update_data:
            setattr(experiment, attr, update_data[attr])

    if 'columns' in update_data:
        await update_columns(experiment, update_data['columns'], session=session)

    if 'measurements' in update_data:
        update_measurements(experiment, update_data['measurements'])

    return construct_lab_experiment_details(experiment)


async def update_columns(experiment: LaboratoryExperiment, columns: list[dict], session: AsyncSession) -> None:
    current_columns = {col.name: col for col in experiment.columns}
    incoming_names = {col['name'] for col in columns}

    experiment.columns[:] = [col for col in experiment.columns if col.name in incoming_names]

    await check_ontologies(columns)
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


@connection
async def update_comp_experiment_data(experiment_id: int,
                                      update: UpdateComputationalExperimentRequest,
                                      session: AsyncSession,
                                      ) -> ComputationalExperimentDetails:
    q = (
        select(ComputationalExperiment)
        .options(
            selectinload(ComputationalExperiment.template),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.input),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.output),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.parameters),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.context),
            selectinload(ComputationalExperiment.data),
            selectinload(ComputationalExperiment.data)
            .selectinload(ComputationalExperimentData.input),
            selectinload(ComputationalExperiment.data)
            .selectinload(ComputationalExperimentData.output),
            selectinload(ComputationalExperiment.data)
            .selectinload(ComputationalExperimentData.parameters),
            selectinload(ComputationalExperiment.data)
            .selectinload(ComputationalExperimentData.context),
        )
        .filter_by(id=experiment_id)
    )

    experiment = (await session.execute(q)).scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EXPERIMENT_NOT_FOUND_MESSAGE)

    update_data = update.model_dump(exclude_unset=True)
    for attr in INFORMATIONAL_ATTRIBUTES:
        if attr in update_data:
            setattr(experiment, attr, update_data[attr])

    if 'data' in update_data:
        existing_data = {d.row: d for d in experiment.data}
        new_data = []

        template = experiment.template

        template_input_schema = template.input.data if template.input else {}
        template_output_schema = template.output.data if template.output else {}
        template_parameters_schema = template.parameters.data if template.parameters else {}
        template_context_schema = template.context.data if template.context else {}

        for i, (input_data, output_data, parameters_data, context_data) in enumerate(update_data['data']):
            current = existing_data.get(i)

            if (current and
                    current.input.data == input_data and
                    current.output.data == output_data and
                    current.parameters.data == parameters_data and
                    current.context.data == context_data
            ):
                new_data.append(current)
            else:
                input = Schema(type=SchemaKind.INPUT, data=input_data)
                output = Schema(type=SchemaKind.OUTPUT, data=output_data)
                parameters = Schema(type=SchemaKind.PARAMETERS, data=parameters_data)
                context = Schema(type=SchemaKind.CONTEXT, data=context_data)
                validate_schema(input_data, template_input_schema, SchemaKind.INPUT)
                validate_schema(output_data, template_output_schema, SchemaKind.OUTPUT)
                validate_schema(parameters_data, template_parameters_schema, SchemaKind.PARAMETERS)
                validate_schema(context_data, template_context_schema, SchemaKind.CONTEXT)

                session.add_all([input, output, parameters, context])
                await session.flush()

                new_data.append(
                    ComputationalExperimentData(
                        row=i,
                        experiment_id=experiment.id,
                        input_id=input.id,
                        output_id=output.id,
                        parameters_id=parameters.id,
                        context_id=context.id,
                    )
                )

        experiment.data[:] = new_data

    await session.flush()
    experiment = (await session.execute(q)).scalar_one_or_none()

    return construct_comp_experiment_details(experiment)


def validate_schema(data: dict, schema: dict, kind: SchemaKind) -> None:
    if set(data.keys()) != set(schema.keys()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f'{kind} data keys do not match template schema: expected {set(schema.keys())}, got {set(data.keys())}'
        )


@connection
async def delete_experiment(experiment_id: int, user: User, session: AsyncSession) -> Response:
    q = select(Experiment).filter_by(id=experiment_id)
    experiment = (await session.execute(q)).scalar_one_or_none()

    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EXPERIMENT_NOT_FOUND_MESSAGE)

    if experiment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=OTHER_EXPERIMENT_DELETING_MESSAGE)

    # await session.delete(experiment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
