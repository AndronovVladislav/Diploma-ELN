from pydantic import BaseModel


class TemplateDetails(BaseModel):
    id: int
    path: str

    input: dict
    output: dict
    parameters: dict
    context: dict
