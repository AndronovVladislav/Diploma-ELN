from fastapi import APIRouter

from backend.schemas.ontologies.om2.requests import UnitShortDetails
from backend.services.ontologies.om2 import get_all_units_short_details as get_all_om2_units_short_details
from backend.services.ontologies.ontologies import (
    get_ontologies_names as get_ontologies_names_service,
)

router = APIRouter(prefix='/ontology', tags=['Ontologies'])


@router.get('/', response_model=list[str])
async def get_ontologies_names():
    return get_ontologies_names_service()


@router.get('/om2', response_model=list[UnitShortDetails])
async def get_om2_units_short_details():
    result = await get_all_om2_units_short_details()
    return result
