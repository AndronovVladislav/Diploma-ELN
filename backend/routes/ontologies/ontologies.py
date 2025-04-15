from fastapi import APIRouter, HTTPException

from backend.base import ONTOLOGIES_MAPPING
from backend.schemas.ontologies.chebi.requests import UnitShortDetails as ChEBIUnitShortDetails
from backend.schemas.ontologies.om2.requests import UnitShortDetails as OM2UnitShortDetails
from backend.services.ontologies.chebi import get_units_short_details as get_chebi_units_short_details
from backend.services.ontologies.om2 import get_units_short_details as get_om2_units_short_details
from backend.services.ontologies.ontologies import (
    get_ontologies_names as get_ontologies_names_service,
)

router = APIRouter(prefix='/ontology', tags=['Ontologies'])


@router.get('/', response_model=list[str])
async def get_ontologies_names():
    return get_ontologies_names_service()


@router.get('/details/{ontology}',
            response_model=list[OM2UnitShortDetails | ChEBIUnitShortDetails],
            response_model_by_alias=False,
            )
async def get_ontology_details(ontology: str, limit: int = 1500):
    if ontology not in ONTOLOGIES_MAPPING:
        raise HTTPException(status_code=404, detail=f'Unknown ontology {ontology}')

    result = []
    match ontology:
        case 'om2':
            result = await get_om2_units_short_details(limit=limit)
        case 'chebi':
            result = await get_chebi_units_short_details(limit=limit)
    return result
