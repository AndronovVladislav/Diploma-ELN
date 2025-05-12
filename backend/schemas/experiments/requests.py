from typing import Any

from pydantic import BaseModel, ConfigDict

from backend.schemas.experiments.data import ColumnDetails


class Measurement(BaseModel):
    row: int

    model_config = ConfigDict(extra='allow')


class ImportColumn(ColumnDetails):
    id: None = None

    name: str
    ontology: str
    ontology_ref: str
    is_main: bool


class ImportLaboratoryExperiment(BaseModel):
    path: str
    description: str = ''
    columns: list[ImportColumn]
    measurements: list[Measurement]


class CreateLaboratoryExperimentRequest(BaseModel):
    path: str


class CreateComputationalExperimentRequest(BaseModel):
    path: str
    template_id: int


class UpdateLaboratoryExperimentRequest(BaseModel):
    description: str = None
    path: str = None

    measurements: list[Measurement] = None
    columns: list[ColumnDetails] = None


class UpdateComputationalExperimentRequest(BaseModel):
    description: str = None
    path: str = None

    data: list[tuple[dict, dict, dict, dict]] = None


class ImportComputationalTemplate(BaseModel):
    path: str
    input: dict[str, Any]
    output: dict[str, Any]
    parameters: dict[str, Any]
    context: dict[str, Any] | None = None


class ImportComputationalRow(BaseModel):
    input: dict[str, Any]
    output: dict[str, Any]
    parameters: dict[str, Any]
    context: dict[str, Any] | None = None


class ImportComputationalExperiment(BaseModel):
    path: str
    description: str = ''
    template: ImportComputationalTemplate
    data: list[ImportComputationalRow]

    model_config = ConfigDict(extra='ignore')
