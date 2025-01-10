import asyncio
import json

from neo4j import AsyncSession
from polars import DataFrame, col
from pydantic import BaseModel

from backend.ontology.base import neo4j_helper
from backend.ontology.models import ExperimentDescription
from backend.ontology.om2.queries import DIMENSION_KEY, get_all_units


class ColumnDescriptionDTO(BaseModel):
    uri: str
    dimension: str


async def import_experiment(data: ExperimentDescription, session: AsyncSession) -> dict[str, ColumnDescriptionDTO]:
    units = await get_all_units(session)
    result: dict[str, ColumnDescriptionDTO] = {}

    for column, props in data.headers.ontological_description.columns.items():
        filter_col = 'label' if props.key.endswith('@en') else 'symbol'
        unit_spec = units.filter(col(filter_col) == props.key).to_dict()
        result[column] = ColumnDescriptionDTO(uri=unit_spec['uri'][0], dimension=unit_spec[DIMENSION_KEY][0])

    pk = data.headers.ontological_description.primary_key
    df = DataFrame(data.body)
    df.columns.remove(pk)
    df.columns.insert(0, pk)
    return result
