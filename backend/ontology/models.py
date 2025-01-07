from typing import Annotated

from pydantic import BaseModel


class OntologicalDescription(BaseModel):
    database: Annotated[list[str], 'Set of databases for queries to neo4j, in most cases name of ontologies']
    primary_key: Annotated[str, 'A unique column in each row.'
                                'URI of each value from this column will be requested from database.']
    columns: dict[str, Annotated[str, 'A symbol or some part of label of desired ontological type.']]


class HeadersDescription(BaseModel):
    ontological_description: OntologicalDescription


class ExperimentDescription(BaseModel):
    headers: HeadersDescription
    body: Annotated[dict, 'Any dict compatible with polars']