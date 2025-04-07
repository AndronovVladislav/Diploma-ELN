from typing import Annotated

from pydantic import BaseModel


class ColumnOntologicalDescription(BaseModel):
    key: Annotated[str, 'A symbol or label of desired ontological type.']
    ontology: str


class OntologicalDescription(BaseModel):
    primary_key: Annotated[str, 'A unique column in each row.'
                                'URI of each value from this column will be requested from database.']
    columns: dict[str, ColumnOntologicalDescription]


class HeadersDescription(BaseModel):
    ontological_description: OntologicalDescription


class ExperimentDescription(BaseModel):
    headers: HeadersDescription
    body: Annotated[dict, 'Any dict compatible with polars']


class ColumnDetails(BaseModel):
    id: int
    name: str
    ontology: str
    ontology_ref: str


class LaboratoryExperimentDetails(BaseModel):
    name: str
    description: str

    measurements: list[dict]
    columns: list[ColumnDetails]
