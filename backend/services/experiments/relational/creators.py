from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.common.enums import ExperimentKind
from backend.models import User
from backend.models.experiment import LaboratoryExperiment, ComputationalExperiment
from backend.models.utils import connection
from backend.schemas.experiments.data import LaboratoryExperimentDetails, ComputationalExperimentDetails
from backend.services.experiments.relational.utils import construct_lab_experiment_details, \
    construct_comp_experiment_details


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
        .options(
            selectinload(LaboratoryExperiment.columns),
            selectinload(LaboratoryExperiment.measurements)
        )
        .where(LaboratoryExperiment.id == experiment.id)
    )
    full_experiment = (await session.execute(q)).scalar_one()

    return construct_lab_experiment_details(full_experiment)


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

    q = (
        select(ComputationalExperiment)
        .options(
            selectinload(ComputationalExperiment.data),
        )
        .where(ComputationalExperiment.id == experiment.id)
    )
    full_experiment = (await session.execute(q)).scalar_one()

    return construct_comp_experiment_details(full_experiment)
