from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import ExperimentKind
from backend.models import User
from backend.models.experiment import LaboratoryExperiment, Column, Measurement
from backend.models.experiment import (
    Schema, SchemaKind,
    ComputationalExperimentTemplate,
    ComputationalExperiment,
    ComputationalExperimentData,
)
from backend.models.utils import connection
from backend.schemas.experiments.data import ComputationalExperimentDetails
from backend.schemas.experiments.data import LaboratoryExperimentDetails
from backend.schemas.experiments.requests import ImportComputationalExperiment
from backend.schemas.experiments.requests import ImportLaboratoryExperiment
from backend.services.experiments.relational.getters import get_comp_experiment_data
from backend.services.experiments.relational.getters import get_lab_experiment_data
from backend.services.experiments.relational.utils import check_ontologies
from backend.services.experiments.relational.utils import validate_schema


@connection
async def create_lab_experiment(user: User, path: str, session: AsyncSession) -> LaboratoryExperimentDetails:
    experiment = LaboratoryExperiment(
        user_id=user.id,
        path=path,
        description='',
        kind=ExperimentKind.LABORATORY
    )

    session.add(experiment)
    await session.flush()

    return await get_lab_experiment_data(experiment.id, session)


@connection
async def create_comp_experiment(user: User,
                                 path: str,
                                 template_id: int,
                                 session: AsyncSession,
                                 ) -> ComputationalExperimentDetails:
    experiment = ComputationalExperiment(
        user_id=user.id,
        template_id=template_id,
        path=path,
        description='',
        kind=ExperimentKind.COMPUTATIONAL
    )

    session.add(experiment)
    await session.flush()

    return await get_comp_experiment_data(experiment.id, session)


@connection
async def import_laboratory_experiment(user: User,
                                       data: ImportLaboratoryExperiment,
                                       session: AsyncSession,
                                       ) -> LaboratoryExperimentDetails:
    await check_ontologies([item.model_dump() for item in data.columns])

    columns_names = set()
    for col in data.columns:
        if col.name in columns_names:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Имена столбцов не уникальны')
        columns_names.add(col.name)

    for measurement in data.measurements:
        for col in measurement.model_dump():
            if col != 'row' and col not in columns_names:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail='Как минимум одна из ячеек привязана к несуществующему столбцу')

    new_experiment = LaboratoryExperiment(
        description=data.description,
        kind=ExperimentKind.LABORATORY,
        path=data.path,
        user_id=user.id,
    )
    session.add(new_experiment)
    await session.flush()

    columns = [
        Column(name=col.name,
               ontology=col.ontology,
               ontology_ref=col.ontology_ref,
               is_main=col.is_main,
               experiment_id=new_experiment.id,
               )
        for col in data.columns
    ]
    session.add_all(columns)
    await session.flush()

    column_to_id = {col.name: col.id for col in columns}
    measurements = [
        Measurement(row=measurement.row,
                    column=column_to_id[col],
                    value=value,
                    experiment_id=new_experiment.id,
                    )
        for measurement in data.measurements for col, value in measurement.model_dump().items() if col != 'row'
    ]
    session.add_all(measurements)

    await session.commit()
    return await get_lab_experiment_data(new_experiment.id, session)


@connection
async def import_computational_experiment(user: User,
                                          payload: ImportComputationalExperiment,
                                          session: AsyncSession,
                                          ) -> ComputationalExperimentDetails:
    template = payload.template
    input_schema = Schema(type=SchemaKind.INPUT, data=template.input)
    output_schema = Schema(type=SchemaKind.OUTPUT, data=template.output)
    params_schema = Schema(type=SchemaKind.PARAMETERS, data=template.parameters)
    context_schema = Schema(type=SchemaKind.CONTEXT, data=template.context or {})
    session.add_all([input_schema, output_schema, params_schema, context_schema])
    await session.flush()

    comp_template = ComputationalExperimentTemplate(
        user_id=user.id,
        path=template.path,
        input_id=input_schema.id,
        output_id=output_schema.id,
        parameters_id=params_schema.id,
        context_id=context_schema.id,
    )
    session.add(comp_template)
    await session.flush()

    experiment = ComputationalExperiment(
        user_id=user.id,
        template_id=comp_template.id,
        path=payload.path,
        description=payload.description,
        kind=ExperimentKind.COMPUTATIONAL,
    )
    session.add(experiment)
    await session.flush()

    rows: list[ComputationalExperimentData] = []
    for idx, row in enumerate(payload.data):
        validate_schema(row.input, template.input, SchemaKind.INPUT)
        validate_schema(row.output, template.output, SchemaKind.OUTPUT)
        validate_schema(row.parameters, template.parameters, SchemaKind.PARAMETERS)
        validate_schema(row.context or {}, template.context or {}, SchemaKind.CONTEXT)

        in_s = Schema(type=SchemaKind.INPUT, data=row.input)
        out_s = Schema(type=SchemaKind.OUTPUT, data=row.output)
        prm_s = Schema(type=SchemaKind.PARAMETERS, data=row.parameters)
        ctx_s = Schema(type=SchemaKind.CONTEXT, data=row.context or {})
        session.add_all([in_s, out_s, prm_s, ctx_s])
        await session.flush()

        rows.append(ComputationalExperimentData(row=idx,
                                                experiment_id=experiment.id,
                                                input_id=in_s.id,
                                                output_id=out_s.id,
                                                parameters_id=prm_s.id,
                                                context_id=ctx_s.id,
                                                )
                    )

    session.add_all(rows)
    await session.commit()

    return await get_comp_experiment_data(experiment.id, session)
