from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator, with_config
from pydantic.alias_generators import to_snake


def select_only_english_version(texts) -> str | None:
    """
    Выбирает из списка одинаковых строк на разных языках только англоязычную версию, используйте с умом.
    """
    if texts is None:
        return
    elif isinstance(texts, list):
        for string in texts:
            if string.endswith('@en'):
                return string


OnlyEnglishValidator = BeforeValidator(select_only_english_version)


@with_config(ConfigDict(alias_generator=to_snake))
class Unit(BaseModel):
    comment: Annotated[str | None, OnlyEnglishValidator] = None
    uri: str

    symbol: str | None = None
    alternative_symbol: list[str] | None = Field(None, alias='alternativeSymbol')

    label: Annotated[str | None, OnlyEnglishValidator] = None
    alternative_label: Annotated[str | None, OnlyEnglishValidator] = Field(None, alias='alternativeLabel')

    laTeXCommand: Annotated[str | None, OnlyEnglishValidator] = Field(None, alias='latex_command')
    longcomment: Annotated[str | None, OnlyEnglishValidator] = None
    unofficialAbbreviation: list[str] | None = Field(None, alias='unofficial_abbreviation')

    hasFactor: float | None = Field(None, alias='has_factor')
    hasExponent: float | None = Field(None, alias='has_exponent')

    @field_validator('symbol', mode='before')
    def select_only_first(cls, v) -> str | None:
        if isinstance(v, list):
            return v[0]
        elif isinstance(v, (str, None)):
            return v

    @field_validator('label', mode='before')
    def select_only_english_version(cls, v) -> str:
        if isinstance(v, list):
            for string in v:
                if string.endswith('@en'):
                    return string
