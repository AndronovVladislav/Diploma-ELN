from fastapi import APIRouter

from backend.models.ontology.base import get_session
from backend.models.ontology.models import ExperimentDescription
from backend.models.ontology.om2.services import ColumnDescriptionDTO
from backend.models.ontology.om2.services import import_experiment as import_experiment_service

router = APIRouter(prefix="/experiments", tags=["Experiments"])


@router.post('/import')
async def import_experiment(experiment: ExperimentDescription) -> dict[str, ColumnDescriptionDTO]:
    async with get_session() as session:
        return await import_experiment_service(experiment, session)
