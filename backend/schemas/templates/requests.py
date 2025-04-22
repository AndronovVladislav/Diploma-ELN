import re

from pydantic import BaseModel, field_validator, RootModel, ConfigDict

from backend.base import ONTOLOGIES_MAPPING


def is_ontology_ref(value: str) -> bool:
    match_obj = re.match(r'^(?P<ontology>[a-zA-Z0-9_\-]+):(?P<ontology_ref>[a-zA-Z0-9_\-]+)$', value)

    if not bool(match_obj):
        return False

    if match_obj['ontology'] not in ONTOLOGIES_MAPPING:
        return False

    return True


class TemplateSchemaData(RootModel[dict[str, str]]):

    @classmethod
    @field_validator('root')
    def validate_ontology_refs(cls, value: dict[str, str]) -> dict[str, str]:
        for key, val in value.items():
            if not is_ontology_ref(val):
                raise ValueError(f'Поле "{key}" содержит недопустимую онтологическую ссылку: "{val}"')
        return value


class CreateTemplateRequest(BaseModel):
    path: str

    input: TemplateSchemaData
    output: TemplateSchemaData
    parameters: TemplateSchemaData
    context: dict[str, str]


class UpdateTemplateRequest(BaseModel):
    path: str
