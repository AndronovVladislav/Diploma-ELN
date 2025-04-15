from functools import cache

from neo4j import AsyncSession

from backend.base import OntologiesRelatedError, ONTOLOGIES_MAPPING
from backend.ontology.base import connection, CypherQueryBuilder, CypherCondition
from backend.schemas.ontologies.om2.requests import UnitShortDetails

ALL_UNIT_LABELS = (
    'CubicPrefixedMetre',
    'GramPerPrefixedLitre',
    'MetrePerPrefixedSecond-Time',
    'MetrePerPrefixedSecond-TimeSquared',
    'MolePerPrefixedLitre',
    'MolePerPrefixedMetre',
    'PrefixedGramPerLitre',
    'PrefixedMetrePerSecond-Time',
    'PrefixedMetrePerSecond-TimeSquared',
    'PrefixedMolePerMetre',
    'PrefixedMolePerLitre',
    'PrefixedSecond-TimeSquared',
    'PrefixedUnit',
    'SingularUnit',
    'SquarePrefixedMetre',
    'Unit',
    'UnitDivision',
    'UnitExponentiation',
    'UnitMultiplication',
)
ALL_UNIT_LABELS = tuple(map(lambda x: f'`{x}`', ALL_UNIT_LABELS))

ONTOLOGY_NAME = 'om2'
NODE_KEY = 'node'
DIMENSION_KEY = 'dimension'

builder = CypherQueryBuilder()


class OM2OntologyMissing(OntologiesRelatedError):
    message = f'Key {ONTOLOGY_NAME} is missing from mapping needed to identify this ontology in Neo4j.'


@cache
def get_match_all_units_query(limit: int) -> str:
    if ONTOLOGY_NAME in ONTOLOGIES_MAPPING:
        return (
            builder
            .match(f'(n:{'|'.join(ALL_UNIT_LABELS)})-[:HASDIMENSION]->(m)')
            .where(CypherCondition(f'n:{ONTOLOGIES_MAPPING[ONTOLOGY_NAME]}'))
            .limit(limit)
            .return_(f'n AS {NODE_KEY}, m.label AS {DIMENSION_KEY}')
            .build()
        )
    raise OM2OntologyMissing


@connection
async def get_units_short_details(limit: int, session: AsyncSession) -> list[UnitShortDetails]:
    return [UnitShortDetails.model_validate({**unit.data()[NODE_KEY], DIMENSION_KEY: unit.data()[DIMENSION_KEY]})
            async for unit in await session.run(get_match_all_units_query(limit))]
