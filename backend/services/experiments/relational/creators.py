from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.common.enums import ExperimentKind
from backend.models import User
from backend.models.experiment import LaboratoryExperiment
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails
from backend.services.experiments.relational.utils import construct_lab_experiment


async def create_user_experiment(user: User, path: str, kind: ExperimentKind) -> LaboratoryExperimentDetails:
    match kind:
        case ExperimentKind.LABORATORY:
            return await create_lab_experiment(user, path)
        case _:
            raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail='Invalid experiment kind')


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

    q = (
        select(LaboratoryExperiment)
        .where(LaboratoryExperiment.id == experiment.id)
        .options(
            selectinload(LaboratoryExperiment.columns),
            selectinload(LaboratoryExperiment.measurements)
        )
    )
    result = await session.execute(q)
    full_experiment = result.scalar_one()

    return construct_lab_experiment(full_experiment)
