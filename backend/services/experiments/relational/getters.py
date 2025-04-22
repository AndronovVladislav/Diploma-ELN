from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.common.enums import ExperimentKind
from backend.models import User
from backend.models.experiment import LaboratoryExperiment, Experiment, ComputationalExperiment
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails
from backend.services.experiments.relational.utils import to_dict, construct_lab_experiment_details


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
async def get_experiment_data(experiment_id: int, session: AsyncSession) -> LaboratoryExperimentDetails | None:
    experiment = await session.get(Experiment, experiment_id)
    if not experiment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Эксперимент с таким id не найден')

    match experiment.kind:
        case ExperimentKind.LABORATORY:
            return await get_lab_experiment_data(experiment_id, session=session)


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Эксперимент с таким id не найден')

    return construct_lab_experiment_details(experiment)
