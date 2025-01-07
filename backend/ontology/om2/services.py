import copy
from types import GenericAlias

from neo4j import AsyncSession
from polars import DataFrame

from ontology.base import ExperimentDescription
from ontology.om2.queries import get_all_units


def _get_schema(objects: list[dict]) -> dict[str, GenericAlias]:
    scheme = {}
    for obj in objects:
        for k, v in obj.items():
            if isinstance(v, list):
                scheme[k] = type(v)[type(v[0])]
            elif k not in scheme:
                scheme[k] = type(v)
    return scheme


def _convert_to_schema(objects: list[dict], schema: dict[str, GenericAlias]) -> list[dict]:
    result = copy.deepcopy(objects)
    for obj in result:
        for k, v in obj.items():
            if type(schema[k]) is GenericAlias and schema[k].__origin__ is list and not isinstance(v, list):
                obj[k] = [v]
    return result


async def import_experiment(data: ExperimentDescription, session: AsyncSession) -> dict:
    units = [_get_only_english_versions(unit) for unit in await get_all_units(session)]
    schema = _get_schema(data.body)
    headers = DataFrame(_convert_to_schema(data.headers.ontological_description.columns))
    
    df = DataFrame(data.body)
    # TODO: convert df to narrow form
    # df.write_database()