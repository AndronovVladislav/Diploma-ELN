from neo4j import AsyncSession
from polars import DataFrame

from backend.ontology.om2.models import UnitWithDimension

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

NODE_KEY = 'node'
DIMENSION_KEY = 'dimension'

MATCH_ALL_UNITS = f'''
MATCH (n:{'|'.join(ALL_UNIT_LABELS)})-[:HASDIMENSION]->(m)
RETURN n AS {NODE_KEY}, m.label AS {DIMENSION_KEY};
'''


async def get_all_units(session: AsyncSession) -> DataFrame:
    return DataFrame(
        [UnitWithDimension.model_validate({**unit.data()[NODE_KEY], DIMENSION_KEY: unit.data()[DIMENSION_KEY]})
         async for unit in await session.run(MATCH_ALL_UNITS)]
    )
