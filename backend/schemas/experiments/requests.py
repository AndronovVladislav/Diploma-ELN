from pydantic import BaseModel

from backend.schemas.experiments.data import ColumnDetails


class UpdateLaboratoryExperimentRequest(BaseModel):
    name: str = None
    description: str = None

    measurements: list[dict] = None
    columns: list[ColumnDetails] = None
