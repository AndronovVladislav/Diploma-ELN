from fastapi import APIRouter, Query

from backend.models.ontology.base import get_session
from backend.models.ontology.models import ExperimentDescription
from backend.models.ontology.om2.services import ColumnDescriptionDTO
from backend.models.ontology.om2.services import import_experiment as import_experiment_service
from backend.routes.experiments.utils import flat_to_tree
from backend.services.experiments import get_user_experiments as get_user_experiments_service

router = APIRouter(prefix="/experiment", tags=["Experiments"])


@router.get('/')
async def get_user_experiments(username: str, desired_keys: list[str] = Query()) -> list[dict]:
    return flat_to_tree(await get_user_experiments_service(username), desired_keys)


@router.post('/import')
async def import_experiment(experiment: ExperimentDescription) -> dict[str, ColumnDescriptionDTO]:
    async with get_session() as session:
        return await import_experiment_service(experiment, session)
