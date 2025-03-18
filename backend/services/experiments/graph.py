from neo4j import AsyncSession
from polars import DataFrame, col

from backend.models.ontology.om2.om2 import UnitWithDimension
from backend.models.utils import connection
from backend.schemas.experiments import ExperimentDescription, ColumnDescription

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


async def import_experiment(data: ExperimentDescription) -> dict[str, ColumnDescription]:
    units = await get_all_units()
    result: dict[str, ColumnDescription] = {}

    for column, props in data.headers.ontological_description.columns.items():
        filter_col = 'label' if props.key.endswith('@en') else 'symbol'
        unit_spec = units.filter(col(filter_col) == props.key).to_dict()
        result[column] = ColumnDescription(uri=unit_spec['uri'][0], dimension=unit_spec[DIMENSION_KEY][0])

    pk = data.headers.ontological_description.primary_key
    df = DataFrame(data.body)
    df.columns.remove(pk)
    df.columns.insert(0, pk)
    return result


@connection
async def get_all_units(session: AsyncSession) -> DataFrame:
    return DataFrame(
        [UnitWithDimension.model_validate({**unit.data()[NODE_KEY], DIMENSION_KEY: unit.data()[DIMENSION_KEY]})
         async for unit in await session.run(MATCH_ALL_UNITS)]
    )
