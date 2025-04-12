from functools import cache

from neo4j import AsyncSession

from backend.base import ONTOLOGIES_MAPPING, OntologiesRelatedError
from backend.ontology.base import connection
from backend.schemas.ontologies.chebi.requests import UnitShortDetails
from backend.services.ontologies.om2 import builder

ONTOLOGY_NAME = 'chebi'
NODE_KEY = 'node'


class ChEBIOntologyMissing(OntologiesRelatedError):
    message = f'Key {ONTOLOGY_NAME} is missing from mapping needed to identify this ontology in Neo4j.'


@cache
def get_match_all_units_query(limit: int) -> str:
    if ONTOLOGY_NAME in ONTOLOGIES_MAPPING:
        return (
            builder
            .match(f'({NODE_KEY}:Class:{ONTOLOGIES_MAPPING[ONTOLOGY_NAME]})')
            .where(f'{NODE_KEY}.label IS NOT NULL')
            .limit(limit)
            .return_(NODE_KEY)
            .build()
        )
    raise ChEBIOntologyMissing


@connection
async def get_units_short_details(limit: int, session: AsyncSession) -> list[UnitShortDetails]:
    return [UnitShortDetails.model_validate(unit.data()[NODE_KEY])
            async for unit in await session.run(get_match_all_units_query(limit))]
