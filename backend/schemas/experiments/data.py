from pydantic import BaseModel, field_validator


class ColumnDetails(BaseModel):
    id: int
    name: str
    ontology: str
    ontology_ref: str
    is_main: bool

    @field_validator('ontology')
    def lowercase_ontology(cls, v: str) -> str:
        return v.lower()


class LaboratoryExperimentDetails(BaseModel):
    id: int
    name: str
    description: str

    measurements: list[dict]
    columns: list[ColumnDetails]


class Schema(BaseModel):
    input: dict
    output: dict
    parameters: dict
    context: dict


class ComputationalExperimentRow(Schema):
    row: int


class ComputationalExperimentTemplate(Schema):
    pass


class ComputationalExperimentDetails(BaseModel):
    id: int
    name: str
    description: str
    template: ComputationalExperimentTemplate

    data: list[ComputationalExperimentRow]
