from pydantic import BaseModel, ConfigDict

from backend.schemas.experiments.data import ColumnDetails


class Measurement(BaseModel):
    row: int

    model_config = ConfigDict(extra='allow')


class CreateLaboratoryExperimentRequest(BaseModel):
    path: str


class CreateComputationalExperimentRequest(BaseModel):
    path: str
    template_id: int


class UpdateLaboratoryExperimentRequest(BaseModel):
    name: str = None
    description: str = None
    path: str = None

    measurements: list[Measurement] = None
    columns: list[ColumnDetails] = None
