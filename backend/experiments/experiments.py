from fastapi import APIRouter

from backend.ontology.base import get_session
from backend.ontology.models import ExperimentDescription
from backend.ontology.om2.services import ColumnDescriptionDTO
from backend.ontology.om2.services import import_experiment as import_experiment_service

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post('/import')
async def import_experiment(experiment: ExperimentDescription) -> dict[str, ColumnDescriptionDTO]:
    async with get_session() as session:
        return await import_experiment_service(experiment, session)
