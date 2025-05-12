from io import BytesIO
from typing import Any

from dicttoxml import dicttoxml
from fastapi import HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.common.enums import ExperimentKind
from backend.models import User
from backend.models.experiment import (
    LaboratoryExperiment,
    Experiment,
    ComputationalExperiment,
    ComputationalExperimentData,
    ComputationalExperimentTemplate,
)
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ComputationalExperimentDetails
from backend.services.experiments.relational.common import EXPERIMENT_NOT_FOUND_MESSAGE
from backend.services.experiments.relational.utils import (
    to_dict,
    construct_lab_experiment_details,
    construct_comp_experiment_details,
    ExportType,
)


@connection
async def get_experiments(username: str, session: AsyncSession) -> list[dict[str, Any]]:
    q = (
        select(User)
        .options(selectinload(User.experiments),
                 selectinload(
                     User.experiments.of_type(ComputationalExperiment)
                 ).selectinload(ComputationalExperiment.template))
        .filter_by(username=username)
    )
    user = (await session.execute(q)).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь с таким id не найден')

    return [to_dict(exp) for exp in user.experiments]


@connection
async def get_experiment_data(experiment_id: int,
                              session: AsyncSession,
                              ) -> LaboratoryExperimentDetails | ComputationalExperimentDetails:
    experiment = await session.get(Experiment, experiment_id)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Эксперимент с таким id не найден')

    match experiment.kind:
        case ExperimentKind.LABORATORY:
            return await get_lab_experiment_data(experiment_id, session)
        case ExperimentKind.COMPUTATIONAL:
            return await get_comp_experiment_data(experiment_id, session)


async def get_lab_experiment_data(experiment_id: int, session: AsyncSession) -> LaboratoryExperimentDetails:
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

    return construct_lab_experiment_details(experiment)


async def get_comp_experiment_data(experiment_id: int, session: AsyncSession) -> ComputationalExperimentDetails:
    q = (
        select(ComputationalExperiment)
        .options(
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.input),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.output),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.parameters),
            selectinload(ComputationalExperiment.template)
            .selectinload(ComputationalExperimentTemplate.context),
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

    return construct_comp_experiment_details(experiment)


@connection
async def export_experiment_data(experiment_id: int,
                                 export_type: ExportType,
                                 session: AsyncSession,
                                 ) -> StreamingResponse:
    q = select(Experiment).where(Experiment.id == experiment_id)

    experiment = (await session.execute(q)).scalar_one_or_none()

    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EXPERIMENT_NOT_FOUND_MESSAGE)

    data = None

    match experiment.kind:
        case ExperimentKind.LABORATORY:
            data = await get_lab_experiment_data(experiment_id, session)
        case ExperimentKind.COMPUTATIONAL:
            data = await get_comp_experiment_data(experiment_id, session)

    intermediate_result = None

    match export_type:
        case ExportType.JSON:
            intermediate_result = data.model_dump_json().encode()
        case ExportType.XML:
            intermediate_result = data.model_dump()
            intermediate_result = dicttoxml(intermediate_result, attr_type=False)

    converted_result = BytesIO()
    converted_result.write(intermediate_result)
    converted_result.seek(0)

    filename = (
        f'{'Laboratory' if experiment.kind == ExperimentKind.LABORATORY else 'Computational'} Experiment'
        f'{experiment.id}.{export_type}'
    )
    return StreamingResponse(
        converted_result,
        media_type='text/plain',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )
