from neo4j import AsyncSession

from ontology.om2.models import Unit

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

RESULT_KEY = 'result'

MATCH_ALL_UNITS = f'''
MATCH (n:{'|'.join(ALL_UNIT_LABELS)})
RETURN n AS {RESULT_KEY};
'''

async def get_all_units(session: AsyncSession) -> list[Unit]:
    return [Unit(unit.data()[RESULT_KEY]) for unit in await session.run(MATCH_ALL_UNITS)]