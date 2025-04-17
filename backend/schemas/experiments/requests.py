from pydantic import BaseModel, ConfigDict

from backend.common.enums import ExperimentKind
from backend.schemas.experiments.data import ColumnDetails


class Measurement(BaseModel):
    row: int

    model_config = ConfigDict(extra='allow')


class CreateExperimentRequest(BaseModel):
    kind: ExperimentKind
    path: str


class UpdateLaboratoryExperimentRequest(BaseModel):
    name: str = None
    description: str = None

    measurements: list[Measurement] = None
    columns: list[ColumnDetails] = None
