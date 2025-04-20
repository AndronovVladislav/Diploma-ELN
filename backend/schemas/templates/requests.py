import re

from pydantic import BaseModel, field_validator, RootModel


def is_ontology_ref(value: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9_\-]+:[a-zA-Z0-9_\-]+$', value))


class TemplateSchemaData(RootModel[dict[str, str]]):

    @classmethod
    @field_validator('root')
    def validate_ontology_refs(cls, value: dict[str, str]) -> dict[str, str]:
        for key, val in value.items():
            if not is_ontology_ref(val):
                raise ValueError(f'Поле "{key}" содержит недопустимую онтологическую ссылку: "{val}"')
        return value


class TemplateCreateRequest(BaseModel):
    path: str

    input: TemplateSchemaData
    output: TemplateSchemaData
    parameters: TemplateSchemaData
    context: dict[str, str]


class TemplateCreateResponse(BaseModel):
    id: int
    input_id: int
    output_id: int
    parameters_id: int
    context_id: int
